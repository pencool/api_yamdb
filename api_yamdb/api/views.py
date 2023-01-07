from api.filters import TitleFilter
from api.permissions import (IsAdminPermission, IsAdminOrReadOnly,
                             IsModeratorPermission,
                             IsOwnerOrReadOnlyPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             CustomTokenSerializer, GenreSerializer,
                             MeUserSerializer, ReviewSerializer,
                             SignupSerializer, TitleEditSerializer,
                             TitleReadSerializer, UserSerializer)
from api.utils import generate_confirm_code
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    """CRUD пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'delete', 'post']
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdminPermission,)

    @action(methods=['get', 'patch'], detail=False,
            queryset=User.objects.all(),
            permission_classes=(IsAuthenticated,)
            )
    def me(self, request):
        cur_user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = MeUserSerializer(cur_user, data=request.data,
                                          partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(cur_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Создание пользователя или получение кода доступа для уже
    зарегистрированного пользователя."""

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        bad_answer = {
            "username": ["Must be filled"],
            "email": ["Must be filled"]
        }
        if username is None:
            return Response(bad_answer, status=status.HTTP_400_BAD_REQUEST)
        elif email is None:
            return Response(bad_answer, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=request.data['username'],
                               email=request.data['email']).exists():
            code = generate_confirm_code()
            User.objects.filter(username=request.data['username']).update(
                confirmation_code=code)
            return Response(status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)


class CustomToken(APIView):
    """Получение токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Invalid confirmation_code'},
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnlyPermission | IsModeratorPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        request_title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return request_title.reviews.all()

    def perform_create(self, serializer):
        request_title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=request_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnlyPermission | IsModeratorPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        request_review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return request_review.comments.all()

    def perform_create(self, serializer):
        request_review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=request_review)
