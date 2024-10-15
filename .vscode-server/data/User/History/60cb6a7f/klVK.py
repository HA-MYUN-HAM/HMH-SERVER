from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Event, UserApplication

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class KakaoTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    code = serializers.CharField()


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "position", "profile_image")


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "position", "profile_image")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_title', 'event_image_url', 'event_date', 'event_time', 'event_location', 'event_info']


class UserApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApplication
        fields = ['id', 'user', 'event', 'applied_at']
        read_only_fields = ['applied_at']
