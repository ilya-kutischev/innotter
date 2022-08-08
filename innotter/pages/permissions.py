from rest_framework import permissions
from datetime import datetime


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPageBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(obj.unblock_date > datetime.now())


class IsPrivatePage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_private


class IsUserActiveAndNotBlockedByToken(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_active and not user.is_blocked)


class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.Roles == "moderator")