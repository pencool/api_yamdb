from random import sample
from string import ascii_letters, digits
from django.core.mail import send_mail
from yamdb.models import User


def generate_confirm_code():
    return ''.join(sample(ascii_letters + digits, 20))


# def send_confirm_email(user: User):
#     send_mail('Подтверждение регистрации.'
#               f'Привет {user.username}, используйте этот код '
#               f'{user.confirmation_code}, для регистрации на Yamdb!',
#               f'admin@yamdb.ru',
#               [f'{user.email}'],
#               fail_silently=False)


user = User.objects.filter(username='admin')

#send_confirm_email(user)
