from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """Содержит пользователей."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    )
    username = models.CharField(verbose_name='никнейм', max_length=150, unique=True, db_index=True)
    email = models.EmailField(verbose_name='email', max_length=254, unique=True)
    bio = models.TextField(verbose_name='биография', null=True)
    role = models.CharField(verbose_name='роль', max_length=10, choices=ROLE_CHOICES, default=USER)

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Содержит категории произведений."""
    name = models.CharField(verbose_name='название категории', max_length=256)
    slug = models.SlugField(verbose_name='сокращение категории', unique=True, max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Содержит жанры произведений."""
    name = models.CharField(verbose_name='название жанра', max_length=256)
    slug = models.SlugField(verbose_name='сокращение жанра', unique=True, max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Содержит произведения."""
    name = models.TextField(verbose_name='произведение')
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0, 'Год произведения не может быть отрицательным!'),
            MaxValueValidator(2022, 'Нельзя публиковать произведения из будущего!')
        ],
        verbose_name='год'
    )
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='категория'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Содержит обзоры на произведения."""
    text = models.TextField(verbose_name='текст отзыва')
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!')
        ],
        verbose_name='оценка произведения'
    )
    pub_date = models.DateTimeField(verbose_name='дата публикации отзыва', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(fields=['title', 'author'], name='unique')]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Содержит комментарии к отзывам."""
    text = models.TextField(verbose_name='текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор комментария'
    )
    pub_date = models.DateTimeField(verbose_name='дата публикации комментария', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
