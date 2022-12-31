from random import sample
from string import ascii_letters, digits
from django.core.mail import send_mail


def generate_confirm_code():
    return ''.join(sample(ascii_letters + digits, 20))


def send_confirm_email(conf_code, username, email):
    send_mail(subject=f'Yamdb Verification.',
              message=f'Привет {username}, используйте этот код '
              f'{conf_code}, для регистрации на Yamdb!',
              from_email='admin@yamdb.ru',
              recipient_list=[f'{email}'],
              fail_silently=False)
