from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
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

    # 이미 신청했는지 확인
    existing_application = UserApplication.objects.filter(user=request.user, event=event).exists()
    if existing_application:
        return Response({"error": "이미 이 행사에 신청하셨습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 신청 처리
    application = UserApplication.objects.create(user=request.user, event=event)
    return Response({"message": "행사 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

class BannerEventView(APIView):
    def get(self, request, *args, **kwargs):
        # use_as_banner가 True인 이벤트들만 가져오기
        banner_events = Event.objects.filter(use_as_banner=True)
        serializer = EventSerializer(banner_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)