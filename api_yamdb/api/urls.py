from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, CurrentUserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, \
    CommentViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls), name='api-root'),
    path('users/me/', CurrentUserViewSet),
]
