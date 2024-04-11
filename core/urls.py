from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='users')

urlpatterns = router.urls
