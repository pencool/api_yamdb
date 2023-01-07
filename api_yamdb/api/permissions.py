from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """ Права доступа: Суперпользователь или администратор."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа: администратор или чтение"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin'))
                )


class IsModeratorPermission(permissions.BasePermission):
    """ Права доступа: модератор или администратор."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
                request.user.role in ['admin', 'moderator']
                or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


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
