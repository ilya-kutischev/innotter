from datetime import datetime
from rest_framework import permissions
from pages.models import Page


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.reply_to == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.kwargs['page'] == request.user


class IsPageOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return Page.objects.get(uuid=view.kwargs['page']).owner == request.user


class IsUserBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_blocked


class IsPageBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        UD = Page.objects.get(uuid=view.kwargs['page']).unblock_date
        if UD is None:
            return True

        return bool(UD.replace(tzinfo=None) > datetime.now().replace(tzinfo=None))
