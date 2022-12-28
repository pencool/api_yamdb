from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
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
