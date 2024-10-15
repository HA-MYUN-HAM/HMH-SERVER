from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Team(models.Model):
    team_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

class Event(models.Model):
    team = models.ForeignKey(Team, related_name='events', on_delete=models.CASCADE)
    event_title = models.CharField(max_length=200)
    event_image_url = models.URLField(null=True, blank=True)  # Image URL for the event
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=200)
    event_shortinfo = models.CharField(max_length=2000, null=True, blank=True)  # Short description of the event
    event_info = models.TextField()  # Full description
    event_account = models.CharField(max_length=255, null=True, blank=True)  # Event's bank account details
    contact_phone = models.CharField(max_length=20)
    use_as_banner = models.BooleanField(default=False)  # Whether to use this event for the banner

    def __str__(self):
        return self.event_title

# 이미지 저장
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=2000)
    image_size = models.CharField(max_length=1000)
    image_link = models.URLField(max_length=1000)

    def __str__(self):
        return self.image_name

# 이미지 링크 연결
class EventImage(models.Model):
    event_id = models.ForeignKey(Event, related_name='event_images', on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, related_name='event_images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for event {self.event_id}"

class UserApplication(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_applications', on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, related_name='user_applications', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.username} applied for {self.event_id.event_name}"

class Ticket(models.Model):
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.event.event_title} - {self.user.username}'