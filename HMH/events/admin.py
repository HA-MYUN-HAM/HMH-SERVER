from django.contrib import admin
from .models import Team, Event, Ticket

class EventInline(admin.TabularInline):
    model = Event
    extra = 1  # Number of extra forms to display when creating a team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'created_at')
    inlines = [EventInline]  # Allows you to add events directly from the team page

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'team', 'event_date', 'event_time', 'event_location', 'use_as_banner')
    list_filter = ('team', 'event_date', 'use_as_banner')  # Filters in the admin interface
    search_fields = ('event_title', 'team__team_name')  # Search by event title and team name

class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'issued_at')
    list_filter = ('event', 'issued_at')
    search_fields = ('user__username', 'event__event_title')  # Search by username and event title

admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)