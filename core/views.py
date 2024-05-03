from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import TeacherSerializer
from .models import Teacher

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True).exclude(is_student=True).order_by("last_name", "first_name", "status")
    serializer_class = TeacherSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
