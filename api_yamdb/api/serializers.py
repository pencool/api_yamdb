from rest_framework import serializers
from api.utils import generate_confirm_code
from api.utils import send_confirm_email
from rest_framework.validators import UniqueValidator
from yamdb.models import User


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

        return data


class MeUserSerializer(UserSerializer):
    role = serializers.CharField(max_length=50, read_only=True)


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all())])

    class Meta:
        fields = ('username', 'email')
        model = User

    def create(self, validated_data):
        send_confirm_email(**validated_data)
        user = User.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        if attrs['username'].lower() == 'me':
            raise serializers.ValidationError('me запрещено в качесвте '
                                              'имени пользователя!')
        attrs['confirmation_code'] = generate_confirm_code()
        return attrs


class CustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True,
                                     required=True)
    confirmation_code = serializers.CharField(max_length=250,
                                              write_only=True, required=True)

    def validate(self, attrs):
        if attrs.get('username') is None:
            raise serializers.ValidationError('u')
        if not User.objects.filter(
                username=attrs['username'],
                confirmation_code=attrs['confirmation_code']).exists():
            raise serializers.ValidationError('Пользователя с таким именем '
                                              'или кодом подтверждения не '
                                              'существует.')
        return attrs

    def create(self, validated_data):
        return validated_data
