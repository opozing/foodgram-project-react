from django.urls import include, path
from django.contrib.auth import get_user_model

from rest_framework.routers import DefaultRouter

from . import views
User = get_user_model()

router = DefaultRouter()
router.register('', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<str:pk>/', views.UserDetailViewSet.as_view({'get': 'list'})),
]