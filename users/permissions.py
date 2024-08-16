from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверяет, является ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsSelfUser(BasePermission):
    """Проверяет, является ли пользователь собой"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user
