from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, GroupViewSet, ExpenseViewSet

router = DefaultRouter()
router.register('subjects', SubjectViewSet, basename='subject')
router.register('groups', GroupViewSet, basename='group')
router.register('expenses', ExpenseViewSet, basename='expense')

urlpatterns = [] + router.urls
