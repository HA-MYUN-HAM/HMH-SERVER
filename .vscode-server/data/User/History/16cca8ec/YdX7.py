from rest_framework import serializers
from .models import Team, Event

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