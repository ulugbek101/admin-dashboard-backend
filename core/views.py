from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import permissions

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Viewset for managing user objects.

    Attributes:
        queryset: Queryset representing active user objects.
        serializer_class: Serializer class for user objects.
        permission_classes: List of permission classes required for accessing this viewset.

    Methods:
        None
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrIsSuperuser]
