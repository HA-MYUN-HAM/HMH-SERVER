from django.urls import path
from . import views

urlpatterns = [
    path('teams/<int:team_id>/', views.team_main_page, name='team_main_page'),
    path('teams/<int:team_id>/events/<int:event_id>/', views.event_details, name='event_details'),
    path('teams/<int:team_id>/events/<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
]
