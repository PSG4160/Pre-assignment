from rest_framework import serializers
from .models import User
from .errors import ERRORS  # 에러 메시지

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'nickname')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호 숨김

    def validate_username(self, value):
        """중복된 username 체크"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(ERRORS["USER_ALREADY_EXISTS"]["message"])
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)