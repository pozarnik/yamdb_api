from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, \
    CommentViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'v1/users', UserViewSet, basename='users')
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
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
