from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment
from rest_framework.validators import UniqueValidator


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать имя <me>!')
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    confirmation_code = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        fields = ('username', 'confirmation_code', 'token')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать имя <me>!')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        unique_together = ('username', 'email')


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = 'id'
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')
        exclude = 'id'
        unique_together = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        exclude = 'id'
        unique_together = ('slug',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('pub_date', 'review')
