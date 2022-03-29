from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User, Category, Genre, Title, Review
from . import serializers
from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly


class SignupAPIView(APIView):
    """Создает пользователя."""
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username, user_email = serializer.validated_data['username'], serializer.validated_data['email']
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'Активация учетной записи {username}',
            f'Код подтверждения {confirmation_code}',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    """Получение токена пользователем."""
    serializer_class = serializers.TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, confirmation_code = serializer.initial_data['username'], serializer.initial_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Возвращает список всех пользователей."""
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class MeAPIView(APIView):
    """Возвращает текущего пользователя."""
    serializer_class = serializers.MeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = self.request.user
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Возвращает список всех категорий, создает и удаляет категории."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CategoryViewSet):
    """Возвращает список всех жанров, создает и удаляет жанры."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Возвращает список всех произведений, создает, обновляет и удаляет произведения."""
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return serializers.TitleCreateSerializer
        return serializers.TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Возвращает список всех отзывов, создает, обновляет и удаляет отзывы к произведениям."""
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        if Review.objects.filter(author=user, title=title).exists():
            raise ValidationError('Нельзя отставлять больше одного отзыва к произведению')
        serializer.save(author=user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Возвращает список всех комментариев, создает, обновляет и удаляет комментарии к отзывам."""
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
