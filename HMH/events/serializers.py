from rest_framework import serializers
from .models import Team, Event, Ticket



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'team_id', 'event_title', 'event_image_url', 'event_date', 
            'event_time', 'event_location', 'event_shortinfo', 'event_info', 
            'event_account', 'contact_phone', 'use_as_banner'
        ]

class TeamSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'team_name', 'created_at', 'events']
    def get_events(self, obj):
        return obj.events.values('id', 'event_title', 'event_image_url', 'event_date', 'event_location')
        

class TicketSerializer(serializers.ModelSerializer):
    
    user = serializers.StringRelatedField(read_only=True)
    event = EventSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'event', 'user', 'issued_at']

class CheckTicketSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    events = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['ticket', 'id','user', 'events', 'issued_at']
        read_only_fields = ['issued_at', 'user']
    def get_events(self, obj):
        event = obj.event
        return [
            {
                'event_id': event.id,
                'event_title': event.event_title,
                'event_image_url': event.event_image_url,
                'event_date': event.event_date,
                'event_time': event.event_time,
                'event_location': event.event_location,
                'event_shortinfo': event.event_shortinfo
            }
        ]
