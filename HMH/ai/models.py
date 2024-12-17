from django.db import models
from events.models import Event

class EventImage(models.Model):
    #event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=1000)
    description = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.event_title} - {self.created_at}"