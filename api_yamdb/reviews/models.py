from api.validators import year_validator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core import validators
from django.db import models
from django.conf import settings

USER_ROLE_CHOICE = (
    (settings.ADMIN, 'Администратор'),
    (settings.MODER, 'Модератор'),
    (settings.USER, 'Пользователь'),
)


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not username:
            raise ValueError('username must be filled.')
        if not email:
            raise ValueError('email must be filled.')
        if username.lower() == 'me':
            raise ValueError("me can't use ase username.")
        user = self.model(username=username,
                          email=self.normalize_email(email),
                          **kwargs
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Кастомная модель User."""

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICE,
                            default='user')
    confirmation_code = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == settings.USER

    @property
    def is_moder(self):
        return self.role == settings.MODER

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название категории', )
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(validators=[year_validator],
                                            verbose_name='Год выхода')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField('Genre', through='TitleGenre',
                                   related_name='genre', verbose_name='Жанр')
    category = models.ForeignKey('Category', blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='category',
                                 verbose_name='Категория')

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        blank=False,
        null=False,
        validators=(
            validators.MinValueValidator(
                1, message="Value can't be a less then 1."),
            validators.MaxValueValidator(
                10, message="Value can't be a more then 10."))
    )

    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='one review per user'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(blank=False, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
