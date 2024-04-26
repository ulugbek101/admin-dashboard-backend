from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register(prefix='teachers', viewset=TeacherViewSet, basename='users')

urlpatterns = router.urls
