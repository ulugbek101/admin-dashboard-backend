from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from .serializers import TeacherSerializer, SubjectSerializer
from .models import Subject

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True).exclude(
        is_student=True).order_by("last_name", "first_name", "status")
    serializer_class = TeacherSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
