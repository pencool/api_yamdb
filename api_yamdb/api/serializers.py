from api.utils import generate_confirm_code, send_confirm_email
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Сериалайзе для пользователя"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate(self, data):
        if data.get('username') in ['me', 'Me', 'mE', 'ME']:
            raise serializers.ValidationError("me can't use ase username.")

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
            raise serializers.ValidationError("me can't use ase username.")
        attrs['confirmation_code'] = generate_confirm_code()
        return attrs


class CustomTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения токена"""
    username = serializers.CharField(max_length=150, write_only=True,
                                     required=True)
    confirmation_code = serializers.CharField(max_length=250, write_only=True,
                                              required=True)


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = get_object_or_404(
                Title,
                pk=self.context.get('view').kwargs.get('title_id')
            )
            user = self.context['request'].user
            if user.reviews.filter(title=title).exists():
                raise serializers.ValidationError('Review already exists')
        return data
