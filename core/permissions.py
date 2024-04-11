from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model

User = get_user_model()


class IsAdmin(BasePermission):
    """
    Custom permission class to check if the user is an administrator.

    Attributes:
        None

    Methods:
        has_permission(self, request, view): Determines whether the user has permission to access the view.
            Returns True if the request method is safe (GET, HEAD, or OPTIONS) or if the user is an admin,
            otherwise returns False.
        has_object_permission(self, request, view, obj): Checks if the user has permission to perform the given
            action on a specific object. Returns True if the user is an admin, otherwise returns False.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class IsSuperuser(BasePermission):
    """
    Custom permission class to check if the user is a superuser.

    Attributes:
        None

    Methods:
        has_permission(self, request, view): Validates whether the user has permission to access the view.
            Returns True if the request method is safe (GET, HEAD, or OPTIONS) or if the user is a superuser,
            otherwise returns False.
        has_object_permission(self, request, view, obj): Checks if the user has permission to perform the given
            action on a specific object. Returns True if the user is a superuser, otherwise returns False.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsAdminOrIsSuperuser(BasePermission):
    """
    Custom permission class to allow access to admin and superuser actions.

    This permission class grants permissions based on the user's role and the type of request.

    Attributes:
        None

    Methods:
        has_permission(self, request, view): Determines whether the user has permission to access the view.
            Returns True if the request method is safe (GET, HEAD, or OPTIONS), or if the user is a superuser
            or admin and is making a POST or DELETE request, or if the user is updating their own profile (PUT
            or PATCH), otherwise returns False.
        has_object_permission(self, request, view, obj): Checks if the user has permission to perform the given
            action on a specific object. Returns True if the request method is safe (GET, HEAD, or OPTIONS),
            or if the user is updating their own profile (PUT or PATCH), or if the user is a superuser or admin
            and is updating another user's profile, otherwise returns False.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ['POST', 'DELETE']:
            return request.user.is_superuser or request.user.is_admin

        if request.method in ['PUT', 'PATCH']:
            user = User.objects.get(pk=view.kwargs['pk'])
            if request.user == user:
                return True
            return request.user.is_superuser or request.user.is_admin

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return request.user == obj or request.user.status in ['admin', 'superuser']

        return False
