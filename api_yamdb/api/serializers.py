from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """Создает пользователя."""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать имя <me>!')
        return value


class LoginSerializer(serializers.Serializer):
    """Возвращает токен пользователя."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)


class UsersSerializer(serializers.ModelSerializer):
    """Возвращает список всех пользователей, создает пользователя админом."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать имя <me>!')
        return value


class MeSerializer(serializers.ModelSerializer):
    """Возвращает текущего пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать имя <me>!')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Возвращает список всех категорий, создает и удаляет категории."""

    class Meta:
        model = Category
        exclude = ('id',)
        unique_together = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Возвращает список всех жанров, создает и удаляет жанры."""

    class Meta:
        model = Genre
        exclude = ('id',)
        unique_together = ('slug',)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Создает произведения."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Возвращает список всех произведений, обновляет и удаляет произведения."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Возвращает список всех отзывов, создает, обновляет и удаляет отзывы к произведениям."""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    """Возвращает список всех комментариев, создает, обновляет и удаляет комментарии к отзывам."""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date', 'review')
