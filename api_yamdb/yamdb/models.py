from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICE = (
    ('Администратор', 'admin'),
    ('Модератор', 'moderator'),
    ('Пользователь', 'user'),
)


class User(AbstractUser):
    """Кастомная модель User"""
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICE,
                            default='user')
    confirmation_code = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_fields'),
        ]

    def __str__(self):
        return self.username
