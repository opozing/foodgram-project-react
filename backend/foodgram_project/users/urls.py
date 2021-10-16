from django.urls import include, path
from django.contrib.auth import get_user_model

from rest_framework.routers import DefaultRouter

from . import views
User = get_user_model()

router = DefaultRouter()
router.register('', views.ReUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
