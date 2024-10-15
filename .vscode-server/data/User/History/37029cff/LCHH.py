from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Team, Event, Ticket
from .serializers import TeamSerializer, EventSerializer, TicketSerializer

@api_view(['GET'])
def team_main_page(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team)
    return Response(serializer.data)

@api_view(['GET'])
def event_details(request, team_id, event_id):
    try:
        event = Event.objects.get(team_id=team_id, pk=event_id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['POST'])
def event_registration(request, team_id, event_id):
    try:
        event = Event.objects.get(team_id=team_id, pk=event_id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if event.tickets.count() >= event.max_participants:
        return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)

    ticket = Ticket.objects.create(event=event, user=request.user)
    return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
