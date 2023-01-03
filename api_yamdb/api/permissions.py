from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """ Права доступа: Суперпользователь или администратор."""

    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class IsOwnerAdminAdminPermission(permissions.BasePermission):
    """ Права доступа: Автор отзыва, модератор или администратор."""
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return (request.user.role == 'admin' or request.user.is_superuser
                or 'moderator')
