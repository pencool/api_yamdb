from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from yamdb.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import (UserSerializer, SignupSerializer,
                             CustomTokenSerializer, MeUserSerializer )
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsAdminPermission
from api.utils import generate_confirm_code
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
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


# @api_view(['POST'])
# def SignupViewSet(request):
#     serializer = SignupSerializer(data=request.data)
#     username = request.data.get('username')
#     email = request.data.get('email')
#     if serializer.is_valid():
#         user = User.objects.filter(username=username)
#         if not user.exists():
#             User.objects.create(username=user, email=email)
#         user.update(confirmation_code=generate_confirm_code())
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        if username is None:
            return Response({"username": "Must be filled"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif email is None:
            return Response({"email": "Must be filled"},
                            status=status.HTTP_400_BAD_REQUEST)
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
    permission_classes = (AllowAny,)

    def post(self, request):
        # if not User.objects.filter(
        #         username=request.data.get('username')).exists():
        #     return Response('123', status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, username=request.data['username'])
        serializer = CustomTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #user = get_object_or_404(User, username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            answer = {'access': str(refresh.access_token)}
            return Response(answer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
