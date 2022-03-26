from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, Category, Genre, Title, Review, Comment


class SignupSerializer(serializers.ModelSerializer):
    """Предназначен для создания пользователя"""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать имя <me>!')
        return value


class TokenSerializer(serializers.ModelSerializer):
    """Прендназначен для получения токена пользователем"""
    confirmation_code = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UsersSerializer(SignupSerializer):
    """Предназначен для отображения всех пользователей"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class MeSerializer(SignupSerializer):
    """Предназначен для отображения текущего пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Предназначен для создания и просмотра категорий"""

    class Meta:
        model = Category
        exclude = ('id',)
        unique_together = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Предназначен для создания и просмотра жанров"""

    class Meta:
        model = Genre
        exclude = ('id',)
        unique_together = ('slug',)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Предназначен для создания произведения"""
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
    """Предназначен для отображения произведений"""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        try:
            rating = obj.reviews.aggregate(Avg('score'))
            return rating.get('score__avg')
        except TypeError:
            return None


class ReviewSerializer(serializers.ModelSerializer):
    """Предназначен для создания и просмотра отзывов к произведениям"""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    """Предназначен для создания и просмотра комментариев к отзывам на произведения"""
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date', 'review')
