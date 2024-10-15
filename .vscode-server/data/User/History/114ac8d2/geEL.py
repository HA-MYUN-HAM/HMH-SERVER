import os

import environ
from pathlib import Path

from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view

# 환경변수 세팅
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / ".env"
if not env_file.exists():
  raise ValueError(f"{env_file=} does not exists")
if os.getenv("DJANGO_ENV") == "production":
    env_file = BASE_DIR / ".env.prod"
env = environ.Env()
env.read_env(env_file)

KAKAO_CALLBACK_URI = "https://127.0.0.1:8000/accounts/kakao/callback"
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



class KakaoLoginView(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI