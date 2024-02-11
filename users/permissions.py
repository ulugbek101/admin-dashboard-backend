from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access for all users.
    Allow creating accounts for superusers.
    Allow update and delete only if the user is the owner.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        elif request.method in SAFE_METHODS:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        # print(obj == request.user)
        return request.user.is_superuser or obj == request.user


