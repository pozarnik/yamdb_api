from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, CurrentUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('me/', CurrentUserViewSet),
    path('', include(router.urls), name='api-user'),
]
