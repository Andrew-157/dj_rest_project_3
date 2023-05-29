from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,\
    UserSerializer as BaseUserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'username', 'password',
            'email', 'first_name', 'last_name'
        ]

    def validate_email(self, value):
        # check if user enters email that is not in database
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Duplicate email')
        return value


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name'
        ]

    def validate_email(self, value):
        # check if user enters email that is either their
        # existing email or new email that is not in the database
        current_user = self.context['request'].user
        user_with_email = User.objects.filter(email=value).first()
        if user_with_email and user_with_email != current_user:
            raise serializers.ValidationError('Duplicate email')
        return value
