from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import User
from .serializers import UserSerializer, CurrentUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'


class CurrentUserViewSet(viewsets.ModelViewSet):
    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.get(username=self.request.user)
        return queryset
