from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):  #Категория
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

class Genre(models.Model):    #Жанр
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):    #Произведение/фильм/песня
    name = models.TextField()
    year = models.IntegerField()
    description = models.CharField(null=True,)
    genre = models.ForeignKey(
        Genre,
        related_name='titles',
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL
    )

class Review(models.Model):   # Отзыв
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
    score = models.IntegerField()
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


