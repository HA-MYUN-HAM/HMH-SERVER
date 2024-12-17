from django.urls import path
from .views import EventCreateAPIView, EventDeleteAPIView, EventUpdateAPIView

urlpatterns = [
    path('events/', EventCreateAPIView.as_view(), name='event-create'),
    path('events/<int:event_id>/delete', EventDeleteAPIView.as_view(), name='event-delete'),
    path('events/<int:event_id>/update', EventUpdateAPIView.as_view(), name='event-delete')
]