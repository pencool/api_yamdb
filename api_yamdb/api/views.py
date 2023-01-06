from rest_framework.generics import get_object_or_404
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from .mixins import CustomViewSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from .filters import TitlesFilter
from .permissions import (IsAdminOrReadOnly)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category,
            slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug_in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        serializer.save()
        category = get_object_or_404(
            Category,
            slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug_in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)
