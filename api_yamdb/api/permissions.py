from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """ Права доступа: Суперпользователь или администратор."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа: администратор или чтение"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsModeratorPermission(permissions.BasePermission):
    """ Права доступа: модератор или администратор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and (
                request.user.is_admin or request.user.is_moder))


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    """Права доступа: автор или чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
