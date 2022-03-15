from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = '__all__'
        exclude = 'id'
        unique_together = ('username', 'email')


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = 'id'
        read_only_fields = ('role',)
