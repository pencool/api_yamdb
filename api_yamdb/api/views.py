from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from yamdb.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import (UserSerializer, SignupSerializer,
                             CustomTokenSerializer, MeUserSerializer,
                             RepSingUpSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsAdminPermission
from api.utils import generate_confirm_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
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

    # def get_serializer_class(self):
    #     if User.objects.filter(username=self.request.data['username'],
    #                            email=self.request.data['email']).exists():
    #         return RepSingUpSerializer
    #     return SignupSerializer

    def create(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data['username'],
                               email=request.data['email']).exists():
            serializer = RepSingUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data,
    #                                      partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class CustomToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            answer = {'access': str(refresh.access_token)}
            return Response(answer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
