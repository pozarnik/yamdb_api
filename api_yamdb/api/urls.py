from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()
router.register(r'users', views.UsersViewSet, basename='users')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('auth/token/', views.TokenAPIView.as_view(), name='token'),
    path('users/me/', views.MeAPIView.as_view(), name='current_user'),
    path('', include(router.urls), name='api-root'),
]
