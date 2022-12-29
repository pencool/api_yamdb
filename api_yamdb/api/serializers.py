from abc import ABC

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.utils import generate_confirm_code
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
            )
        ]

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('me запрещено в качесвте '
                                              'имени пользователя!')
        if not re.fullmatch(r'[\w.@+-]+', data['username']):
            raise serializers.ValidationError(' Имя пользователя может '
                                              'содержжать только буквы цифры и'
                                              ' следующие символы @ . + -'
                                              '_')
        return data


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        if not User.objects.filter(**attrs).exist():
            raise serializers.ValidationError('Такого пользователя и '
                                              'email не существует.')
        return attrs

    def create(self, validated_data):
        confirm_code = generate_confirm_code()
        validated_data['confirmation_code'] = confirm_code



class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token

    def validate(self, attrs):
        pass
