from django.urls import path, include
from rest_framework import routers
from api.views import (UserViewSet, SignupViewSet, CustomToken,
                       CategoryViewSet, GenreViewSet, TitleViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth\/signup', SignupViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('api/v1/auth/token/', CustomToken.as_view()),
    path('api/v1/', include(router.urls))
]
