from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from yamdb.models import User
import re


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(max_length=150, validators=[
        UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=254, validators=[
        UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        ]

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('me запрещено в качесвте '
                                              'имени пользователя!')
        if not re.fullmatch(r'[\w.@+-]+', data['username']):
            raise serializers.ValidationError(' Имя пользователя может '
                                              'содержжать только буквы цифры и'
                                              ' следующие символы: @ . + -'
                                              '_')
        return data


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, validators=[
        UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=254, validators=[
        UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate(self, attrs):
        if User.objects.filter(**attrs).exists():
            raise serializers.ValidationError('Такой пользователя и '
                                              'email уже существует.')
        if attrs['username'] == 'me':
            raise serializers.ValidationError('me запрещено в качесвте '
                                              'имени пользователя!')
        if not re.fullmatch(r'[\w.@+-]+', attrs['username']):
            raise serializers.ValidationError(' Имя пользователя может '
                                              'содержжать только буквы цифры и'
                                              ' следующие символы: @ . + -'
                                              '_')
        return attrs


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}
