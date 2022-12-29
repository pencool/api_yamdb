from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from yamdb.models import User
from api.serializers import (UserSerializer, SignupSerializer,
                             CustomTokenObtainSerializer)
from django.shortcuts import get_object_or_404
from api.utils import generate_confirm_code
from api.utils import send_confirm_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=True,
            queryset=User.objects.all(),
            # permisson_classes=[''''''],
            )
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'PATCH':
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        conf_code = generate_confirm_code()
        serializer.save(confirmation_code=conf_code)
        send_confirm_email(conf_code, **self.request.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
