from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team, Event, Ticket
from accounts.models import CustomUser
from .serializers import TeamSerializer, EventSerializer, TicketSerializer, CheckTicketSerializer

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
def event_registration(request, team_id, event_id, user_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({"error": "해당 행사가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
    user = CustomUser.objects.get(pk=user_id)
    event = Event.objects.get(pk=event_id)
    # 이미 티켓이 존재하는지 확인
    if Ticket.objects.filter(user=user, event=event).exists():
        return Response({"error": "이미 신청한 행사입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 티켓 생성
    ticket = Ticket.objects.create(user=user, event=event)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def check_tickets(request, team_id, user_id):
    
    user = CustomUser.objects.get(pk=user_id)
    if Ticket.objects.filter(user=user).exists():
        tickets = Ticket.objects.filter(user=user)
        serializer = CheckTicketSerializer(tickets, many=True)
        return Response(serializer.data)

class BannerEventView(APIView):
    def get(self, request, *args, **kwargs):
        # use_as_banner가 True인 이벤트들만 가져오기
        banner_events = Event.objects.filter(use_as_banner=True)
        serializer = EventSerializer(banner_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)