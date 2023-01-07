from api.views import (CategoryViewSet, CommentViewSet, CustomToken,
                       GenreViewSet, ReviewViewSet, SignupViewSet,
                       TitleViewSet, UserViewSet)
from django.urls import include, path
from rest_framework import routers

v1_router = routers.DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register(r'auth\/signup', SignupViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/token/', CustomToken.as_view()),
    path('v1/', include(v1_router.urls))
]
