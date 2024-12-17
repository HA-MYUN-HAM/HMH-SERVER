from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from events.models import Event
from .serializers import EventSerializer

class EventCreateAPIView(GenericAPIView):
    #permission_classes = [IsAdminUser]  # 관리자만 접근 가능

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            return Response({
                "message": "행사가 성공적으로 생성되었습니다.",
                "event_id": event.id,
                "event_title": event.event_title
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAPIView(APIView):
    #permission_classes = [IsAdminUser]  # 관리자만 접근 가능

    def delete(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            event.delete()
            return Response({
                "message": f"행사({event.event_title})가 성공적으로 삭제되었습니다."
            }, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({
                "error": f"이름이 {event.event_title}인 행사가 존재하지 않습니다."
            }, status=status.HTTP_404_NOT_FOUND)

class EventUpdateAPIView(GenericAPIView):
    #permission_classes = [IsAdminUser]  # 관리자만 접근 가능

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, event_id):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            return Response({
                "message": "행사가 성공적으로 수정되었습니다.",
                "event_id": event.id,
                "event_title": event.event_title
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
