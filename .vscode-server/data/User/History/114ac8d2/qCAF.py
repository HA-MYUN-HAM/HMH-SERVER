import jwt
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


from accountapp.models import AppUser


def kakao_callback(request):
    code = request.GET.get("code")

    # Access Token Request
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&client_secret={CLIENT_SECRET}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )

    token_req_json = token_req.json()

    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_req_json.get("access_token")

    # Email Request
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_data = profile_request.json()

    kakao_account = profile_data.get("kakao_account")
    username = kakao_account["profile"]["nickname"]

    data = {"access_token": access_token, "code": code}
    return JsonResponse(data)