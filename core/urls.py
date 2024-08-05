from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SubjectViewSet

router = DefaultRouter()
router.register(prefix='users', viewset=UserViewSet, basename='users')
router.register(prefix='subjects', viewset=SubjectViewSet, basename='subjects'),

urlpatterns = router.urls
