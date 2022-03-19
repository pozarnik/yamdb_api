from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
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
    path('', include(router.urls), name='api-root'),
    path('v1/auth/signup/', views.SignupViewSet, name='signup'),
    path('v1/auth/token/', views.TokenViewSet, name='token'),
    path('v1/users/', views.UsersViewSet, name='users'),
    path('v1/users/<str:username>/', views.UserViewSet, name='user'),
    path('v1/user/me', views.MeViewSet, name='me'),
]
