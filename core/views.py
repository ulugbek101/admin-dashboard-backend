from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import TeacherSerializer
from .models import Teacher

User = get_user_model()


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherSerializer
