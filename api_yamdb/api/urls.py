from django.urls import path, include
from rest_framework import routers
from api.views import UserViewSet, SignupViewSet, CustomToken

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth\/signup', SignupViewSet)

urlpatterns = [
    path('api/v1/auth/token/', CustomToken.as_view(), name='token_obtain'),
    path('api/v1/', include(router.urls))
]
