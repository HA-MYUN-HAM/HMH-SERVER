import os

import environ
from pathlib import Path

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)

from rest_framework_simplejwt.tokens import RefreshToken

import requests
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from dj_rest_auth.registration.views import SocialLoginView
from .models import Event, UserApplication
from .serializers import (
    UserInfoUpdateSerializer,
    GetUserInfoSerializer, KakaoTokenSerializer,
    EventSerializer,
    UserApplicationSerializer
)
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

# 환경변수 세팅
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / ".env"
if not env_file.exists():
  raise ValueError(f"{env_file=} does not exists")
if os.getenv("DJANGO_ENV") == "production":
    env_file = BASE_DIR / ".env.prod"
env = environ.Env()
env.read_env(env_file)

KAKAO_CALLBACK_URI = "http://127.0.0.1:8000/accounts/kakao/callback"
REST_API_KEY = env("KAKAO_REST_API_KEY")
CLIENT_SECRET = env("KAKAO_CLIENT_SECRET_KEY")



@extend_schema(exclude=True)
def kakao_login(request):
    logger.fatal(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

class KakaoLoginView(APIView):
    serializer_class = KakaoTokenSerializer
    @extend_schema(
        summary="카카오 로그인 마무리",
        description="code (인가 코드)를 post 요청으로 보내면 access token, 유저 정보를 반환합니다. **(id_token은 불필요합니다.)**",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                },
            },
        },
        examples=[
            OpenApiExample(
                response_only=True,
                summary="Response Body Example입니다.",
                name="success_example",
                value={
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0",
                    "user_info": {
                        "user_id": 6,
                        "user_email": "dbsgkdudchlr@naver.com",
                        "user_name": "윤하영",
                        "profile_image": "https://k.kakaocdn.net/dn/cI6qGf/btsCovDyklV/ydaQojxohw6VnLxtcdKwuk/img_640x640.jpg",
                        "is_created": False,
                    },
                },
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 카카오 인가코드를 사용해 access_token 획득
        token_res = requests.get(
            f"http://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&client_secret={CLIENT_SECRET}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
        )
        logger.fatal(token_res)

        if token_res.status_code != 200:
            logger.fatal(token_res.json())
            return Response(
                {"error": "Failed to obtain access token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_json = token_res.json()
        access_token = token_json.get("access_token")

        # 카카오 access_token으로부터 사용자 정보 획득
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_res = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)

        if profile_res.status_code != 200:
            return Response(
                {"error": "Failed to obtain user information"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile_json = profile_res.json()

        kakao_oid = profile_json.get("id")
        nickname = profile_json.get("properties")["nickname"]
        profile_image = profile_json.get("properties")["profile_image"]
        user_email = profile_json.get("kakao_account")["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "user_name": f"{nickname}",
                "kakao_oid": kakao_oid,
                "profile_image": f"{profile_image}",
            },
        )

        # 사용자에 대한 토큰 생성
        refresh = RefreshToken.for_user(user)
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user_info": {
                "user_id": user.id,
                "user_email": user.email,
                "user_name": user.username,
                "profile_image": user.profile_image,
                "is_created": created,
            },
        }

        return Response(data, status=status.HTTP_200_OK)


class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 설정

    @extend_schema(
        summary="유저 정보 업데이트",
        request=UserInfoUpdateSerializer,
        responses={200: UserInfoUpdateSerializer},
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserInfoUpdateSerializer(
            user, data=request.data, partial=True
        )  # 부분 업데이트 가능

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetUserInfoSerializer

    @extend_schema(
        summary="유저 정보 반환",
    )
    def get(self, request):
        user = request.user
        serializer = GetUserInfoSerializer(user)
        return Response(serializer.data)

class ApplyForEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        event = get_object_or_404(Event, pk=event_id)
        application, created = UserApplication.objects.get_or_create(
            user=request.user, event=event
        )
        if not created:
            return Response({"error": "User has already applied for this event."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Successfully applied for the event."}, status=status.HTTP_200_OK)


class EventListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

User = get_user_model()

class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: 현재 로그인한 사용자의 정보 조회
    def get(self, request):
        user = request.user
        serializer = GetUserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT: 사용자 정보 업데이트
    def put(self, request):
        user = request.user
        serializer = UserInfoUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)