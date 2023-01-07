from django.urls import path, include
from rest_framework import routers

from api.views import (UserViewSet, SignupViewSet, CustomToken,
                       CategoryViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auth\/signup', SignupViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('api/v1/auth/token/', CustomToken.as_view()),
    path('api/v1/', include(router.urls))
]
