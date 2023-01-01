from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import serializers
from api.utils import generate_confirm_code
from api.utils import send_confirm_email
from rest_framework.validators import UniqueTogetherValidator
from yamdb.models import User
import re


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
        }
        required_fields = ['username', 'email']

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('me запрещено в качесвте '
                                              'имени пользователя!')
        if not re.fullmatch(r'[\w.@+-]+', data['username']):
            raise serializers.ValidationError(' Имя пользователя может '
                                              'содержжать только буквы цифры и'
                                              ' следующие символы: @ . + -'
                                              '_')

        return data


class MeUserSerializer(UserSerializer):
    role = serializers.CharField(max_length=50, read_only=True)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', 'username')
        model = User
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def create(self, validated_data):
        send_confirm_email(**validated_data)
        return validated_data

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError('me запрещено в качесвте '
                                              'имени пользователя!')
        if not re.fullmatch(r'[\w.@+-]+', attrs['username']):
            raise serializers.ValidationError(' Имя пользователя может '
                                              'содержжать только буквы цифры и'
                                              ' следующие символы: @ . + -'
                                              '_')
        # if not User.objects.filter(
        #         username=attrs['username'],
        #         email=attrs['email']).exists():
        #     raise serializers.ValidationError('Пользователя с таким именем '
        #                                       'или кодом подтверждения не '
        #                                       'существует.')
        attrs['confirmation_code'] = generate_confirm_code()
        return attrs


class CustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    confirmation_code = serializers.CharField(max_length=250, write_only=True)

    def validate(self, attrs):
        if not User.objects.filter(
                username=attrs['username'],
                confirmation_code=attrs['confirmation_code']).exists():
            raise serializers.ValidationError('Пользователя с таким именем '
                                              'или кодом подтверждения не '
                                              'существует.')
        return attrs

    def create(self, validated_data):
        return validated_data
