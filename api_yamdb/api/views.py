from django.shortcuts import get_object_or_404
from yamdb.models import Title, Comment, Review
from rest_framework import permissions, viewsets, filters, mixins

from .permissions import IsOwnerOrReadOnly, IsModeratorPermission
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, IsModeratorPermission,)

    def get_queryset(self):
        request_title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return request_title.comments

    def perform_create(self, serializer):
        request_title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=request_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsModeratorPermission,)

    def get_queryset(self):
        request_review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return request_review.comments

    def perform_create(self, serializer):
        request_review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=request_review)
