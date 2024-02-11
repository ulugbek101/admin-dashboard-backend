from rest_framework import viewsets
from rest_framework.views import Response, APIView, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly
from .serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    """ ViewSet to handle CRUD operations for teachers """

    queryset = get_user_model().objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
