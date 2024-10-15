from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    team_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

class Event(models.Model):
    team = models.ForeignKey(Team, related_name='events', on_delete=models.CASCADE)
    event_title = models.CharField(max_length=255)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.IntegerField()
    contact_phone = models.CharField(max_length=20)
    promotion_image_url = models.URLField(null=True, blank=True)
    use_as_banner = models.BooleanField(default=False)

    def __str__(self):
        return self.event_title

class Ticket(models.Model):
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.event.event_title} - {self.user.username}'
