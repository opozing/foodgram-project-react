from django.urls import include, path
from django.contrib.auth import get_user_model

from rest_framework.routers import DefaultRouter

from . import views
User = get_user_model()

router = DefaultRouter()
router.register('users', views.ReUserViewSet)
# router.register('users/subscriptions', views.SubscriptionViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
