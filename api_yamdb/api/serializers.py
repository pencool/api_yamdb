from rest_framework import serializers
from api.utils import generate_confirm_code
from api.utils import send_confirm_email
from rest_framework.validators import UniqueValidator
from yamdb.models import User, Title, Genre, Category, TitleGenre


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Сериалайзе для пользователя"""

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
    """Сериалайзер для получения данных своей учетной записи"""
    role = serializers.CharField(max_length=50, read_only=True)


class SignupSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации нового пользователя  получения кода
    подтверждения для регистрации"""
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
    """Сериалайзер для получения токена"""
    username = serializers.CharField(max_length=150, write_only=True,
                                     required=True)
    confirmation_code = serializers.CharField(max_length=250, write_only=True,
                                              required=True)


##############################################################################

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleEditSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = ('__all__')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('__all__')
