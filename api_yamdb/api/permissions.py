from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """ Права доступа: Суперпользователь или администратор."""

    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class IsModeratorPermission(permissions.BasePermission):
    """ Права доступа: модератор или администратор."""
    def has_object_permission(self, request, view, obj):
        return (request.user.role in ['admin', 'moderator'] or
                request.user.is_superuser)
