from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from yamdb.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, validators=[
        UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=254, validators=[
        UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role', 'confirmation_code'
                                                      )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_registration_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" запрещено в качесвте '
                                              'имени пользователя!')
        return value
