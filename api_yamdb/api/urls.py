from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet,
                    SignupAPIView, TokenAPIView, UsersViewSet, UserViewSet, MeViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'v1/categories', CategoryViewSet, basename='categories')
router.register(r'v1/genres', GenreViewSet, basename='genres')
router.register(r'v1/titles', TitleViewSet, basename='titles')
router.register(r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls), name='api-root'),
    path('v1/auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
    path('v1/users/', UsersViewSet, name='users'),
    path('v1/users/<str:username>/', UserViewSet, name='user'),
    path('v1/user/me', MeViewSet, name='me'),
]
