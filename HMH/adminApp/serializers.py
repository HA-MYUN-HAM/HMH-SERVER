from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'team', 'event_title', 'event_date', 'event_time', 
            'event_location', 'event_shortinfo', 'event_info', 
            'event_account', 'contact_phone', 'use_as_banner'
        ]
        extra_kwargs = {
            'event_title': {'required': True},
            'event_date': {'required': True},
            'event_location': {'required': True},
        }