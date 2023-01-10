from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(date):
    """Проверка года создания произведения"""
    if date > timezone.now().year:
        raise ValidationError('Год создания не может быть больше текущего.')
