from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.models import Q
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

from api import serializers
from api.filters import TitleFilter
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly
from api_yamdb import settings
from reviews.models import Category, Genre, Title, Review

User = get_user_model()


class SignupAPIView(APIView):
    """Создает пользователя."""

    def __send_email(self, user):
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'Activation',
            f'{user.username}, Ваш код подтверждения {confirmation_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid()
        username = serializer.validated_data.get('username')
        user_email = serializer.validated_data.get('email')
        if User.objects.filter(username=username, email=user_email).exists():
            user = get_object_or_404(User, username=username)
            self.__send_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(Q(username=username) | Q(email=user_email)).exists():
            return Response({"Данный username либо email уже используется"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_user = User.objects.create(username=username, email=user_email)
            self.__send_email(new_user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """Получение токена пользователем."""

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response({"confirmation_code": 'Введен неверный код!'}, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.MeSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = serializers.MeSerializer(
            self.request.user,
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


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Возвращает список всех жанров, создает и удаляет жанры."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Возвращает список всех произведений, создает, обновляет и удаляет произведения."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by('name')
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
        reviews = title.reviews.all()
        return reviews

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
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get("review_id")
        review = title.reviews.get(pk=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get("review_id")
        review = title.reviews.get(pk=review_id)
        serializer.save(author=self.request.user, review=review)
