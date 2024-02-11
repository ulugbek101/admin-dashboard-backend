from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only superusers to create subjects.
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is a superuser for other methods (e.g., POST)
        return request.user.is_superuser
