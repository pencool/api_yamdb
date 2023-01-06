from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from yamdb.models import User
from rest_framework_simplejwt.tokens import AccessToken
from api.serializers import (UserSerializer, SignupSerializer,
                             CustomTokenSerializer, MeUserSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsAdminPermission
from api.utils import generate_confirm_code
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    """CRUD пользователя"""
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
    зарегистрированного пользователя"""
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
    """Получение токена"""
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
