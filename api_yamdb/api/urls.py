import sys
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import UserViewSet

sys.path.append("..")

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/', include(router.urls))
]
