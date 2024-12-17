from rest_framework import serializers
from events.serializers import EventSerializer
from .models import EventImage
from events.models import Event


class EventImageSerializer(serializers.ModelSerializer):
    event_description = serializers.CharField(write_only=True, required=False)
    event = EventSerializer()

    class Meta:
        model = EventImage
        fields = [ 'image_url']
        #read_only_fields = ['id', 'image_url', 'created_at']
