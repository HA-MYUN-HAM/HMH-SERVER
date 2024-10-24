from django.urls import path
from . import views

urlpatterns = [
    path('<int:team_id>/', views.team_main_page, name='team_main_page'),
    path('<int:team_id>/events/<int:event_id>/', views.event_details, name='event_details'),
    path('<int:team_id>/events/<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('<int:team_id>/banner/', views.BannerEventView.as_view(), name='banner_events'),
]
