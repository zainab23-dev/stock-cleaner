from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'items', api_views.TrashViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
