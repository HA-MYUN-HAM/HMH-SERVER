import openai
from openai.error import OpenAIError
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from events.models import Event
import json
import logging

logger = logging.getLogger(__name__)

import os
import environ
from pathlib import Path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EventImageSerializer
from .models import EventImage
from events.models import Event
from rest_framework.generics import GenericAPIView

# 환경변수 세팅
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / ".env"
if not env_file.exists():
  raise ValueError(f"{env_file=} does not exists")
if os.getenv("DJANGO_ENV") == "production":
    env_file = BASE_DIR / ".env.prod"
env = environ.Env()
env.read_env(env_file)


openai.api_key = env("OPENAI_API_KEY")


class EventImageTestView(APIView):
    """이미지 생성 테스트를 위한 HTML 페이지를 렌더링하는 뷰"""
    def get(self, request):
        return render(request, 'test.html')

# Request Serializer 정의
class GenerateImageRequestSerializer(serializers.Serializer):
    event_title = serializers.CharField(required=True, help_text="이벤트 제목")
    event_description = serializers.CharField(required=True, help_text="이벤트 설명")

# Response Serializer 정의
class GenerateImageResponseSerializer(serializers.Serializer):
    image_url = serializers.URLField(help_text="생성된 이미지의 URL")
    message = serializers.CharField(help_text="응답 메시지")

class GenerateImageView(GenericAPIView):
    """이벤트 이미지를 생성하는 API 뷰"""
    '''@swagger_auto_schema(
        query_serializer=GenerateImageRequestSerializer,
        responses={
            status.HTTP_201_CREATED: GenerateImageResponseSerializer,
            status.HTTP_400_BAD_REQUEST: '이벤트 제목과 설명이 필요합니다.',
            status.HTTP_500_INTERNAL_SERVER_ERROR: '이미지 생성 중 오류가 발생했습니다.'
        }
    )'''

    query_set = Event.objects.all()
    serializer_class = GenerateImageRequestSerializer
    
    def post(self, request):
        try:
            event_title = request.data.get('event_title')
            event_description = request.data.get('event_description')

            if not event_title or not event_description:
                return Response({
                    'error': '이벤트 제목과 설명이 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # OpenAI API 호출을 위한 프롬프트 생성
            prompt = (
                f"Create a promotional image for an event titled '{event_title}' "
                f"with details: {event_description}. "
                "The image should be professional and suitable for marketing purposes."
            )

            # OpenAI API를 통한 이미지 생성
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = response['data'][0]['url']

                event_image = EventImage.objects.create(
                    image_url = image_url,
                    description = event_description
                )

                return Response({
                    'image_url': image_url,
                    'message': '이미지가 성공적으로 생성되었습니다.'
                }, status=status.HTTP_201_CREATED)

            except OpenAIError as e:
                logger.error(f"OpenAI API 에러: {str(e)}")
                return Response({
                    'error': '이미지 생성 중 오류가 발생했습니다.',
                    'detail': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"서버 에러: {str(e)}")
            return Response({
                'error': '서버 오류가 발생했습니다.',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SaveImageView(APIView):
    """생성된 이미지를 이벤트에 저장하는 API 뷰"""
    def post(self, request, event_id):
        try:
            event = get_object_or_404(Event, id=event_id)
            image_url = request.data.get('image_url')
            
            if not image_url:
                return Response({
                    'error': '이미지 URL이 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 이벤트 이미지 URL 업데이트
            event.event_image_url = image_url
            event.save()

            return Response({
                'message': '이미지가 성공적으로 저장되었습니다.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"저장 중 오류 발생: {str(e)}")
            return Response({
                'error': '이미지 저장 중 오류가 발생했습니다.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)