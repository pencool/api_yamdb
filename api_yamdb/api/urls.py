from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import UserViewSet, SignupViewSet, CustomTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth\/signup', SignupViewSet)

urlpatterns = [
    path('api/v1/auth/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/', include(router.urls))
]
