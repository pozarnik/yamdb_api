from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):  # Категория
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):  # Жанр
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):  # Произведение/фильм/песня
    name = models.TextField()
    year = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(2022)
        ]
    )
    description = models.TextField(blank=True)
    genre = models.ForeignKey(
        Genre,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )


class Review(models.Model):  # Отзыв
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):  # Коммент
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
