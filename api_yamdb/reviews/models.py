from django.db import models
from .validators import year_validator


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='URL ардеса категории'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='URL адреса жанра'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
        help_text='Используйте формат ввода даты(года) выпуска: YYYY',
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг на основе отзывов',
        null=True,
        default=None
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name
