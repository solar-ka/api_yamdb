from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES_ROLES = (
    ('user', 'юзер'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
    ('superuser', 'суперюзер')
)


class User(AbstractUser):
    role = models.SlugField(
        'роль',
        max_length=16,
        choices=CHOICES_ROLES)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True,
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    genre = models.ManyToManyField(
        Genre, related_name='titles')
    description = models.TextField()

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
