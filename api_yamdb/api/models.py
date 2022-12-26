from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICE = (
    ('Администратор', 'admin'),
    ('Модератор', 'moderator'),
    ('Пользователь', 'user'),
)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICE)


