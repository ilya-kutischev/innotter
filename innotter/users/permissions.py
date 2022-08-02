from rest_framework import permissions
from users.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsUserBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_blocked


class IsUserActiveAndNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(email = request.data['email'])
        return bool(user.is_active and not user.is_blocked)


class IsUserActiveAndNotBlockedByToken(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_active and not user.is_blocked)


class IsOwnerByToken(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
