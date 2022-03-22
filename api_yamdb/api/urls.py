from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'v1/users', views.UsersViewSet, basename='users')
router.register(r'v1/categories', views.CategoryViewSet, basename='categories')
router.register(r'v1/genres', views.GenreViewSet, basename='genres')
router.register(r'v1/titles', views.TitleViewSet, basename='titles')
router.register(r'v1/titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews')
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', views.TokenAPIView.as_view(), name='token'),
    path('v1/users/me/', views.MeAPIView.as_view(), name='current_user'),
    path('', include(router.urls), name='api-root'),
]
