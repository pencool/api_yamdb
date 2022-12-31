from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser
