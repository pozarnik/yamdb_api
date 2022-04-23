from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()
router.register('users', views.UsersViewSet, basename='users')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('token/', views.LoginAPIView.as_view(), name='login'),
]

urlpatterns = [
    path('auth/', include(auth_patterns), name='auth'),
    path('users/me/', views.MeAPIView.as_view(), name='current_user'),
    path('', include(router.urls), name='api-root'),
]
