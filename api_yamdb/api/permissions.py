from rest_framework import permissions


class AnonReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
