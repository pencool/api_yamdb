from random import sample
from string import ascii_letters, digits

from django.core.mail import send_mail
from django.conf import settings


def generate_confirm_code():
    return ''.join(sample(ascii_letters + digits, 20))


def send_confirm_email(confirmation_code, username, email):
    send_mail(subject='Yamdb Verification.',
              message=f'Привет {username}, используйте этот код '
              f'{confirmation_code}, для регистрации на Yamdb!',
              from_email=settings.PROJ_EMAIL,
              recipient_list=[f'{email}'],
              fail_silently=False)
