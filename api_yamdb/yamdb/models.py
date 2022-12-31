from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICE = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


class User(AbstractUser):
    """Кастомная модель User."""
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICE,
                            default='user')
    password = models.CharField(max_length=254, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
