from rest_framework import serializers
from .models import Team, Event, Ticket, UserApplication
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    events = serializers.StringRelatedField(many=True)

    class Meta:
        model = Team
        fields = ['id', 'team_name', 'created_at', 'events']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'team_id', 'event_title', 'event_image_url', 'event_date', 
            'event_time', 'event_location', 'event_shortinfo', 'event_info', 
            'event_account', 'contact_phone', 'use_as_banner'
        ]


class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'event', 'user', 'issued_at']

class UserApplicationSerializer(serializers.ModelSerializer):
    event = EventSerializer()  # 행사 정보도 함께 반환

    class Meta:
        model = UserApplication
        fields = ['id', 'user', 'event', 'applied_at']
        read_only_fields = ['applied_at', 'user']  # applied_at과 user는 읽기 전용

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['team_id','event_id', 'event_title', 'event_image_url', 'event_date', 'event_time', 'event_location']
