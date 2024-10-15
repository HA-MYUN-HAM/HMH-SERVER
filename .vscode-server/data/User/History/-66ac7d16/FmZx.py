from django.urls import include, path, re_path
from .views import kakao_callback, KakaoLogin
#from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
# router = DefaultRouter()

# The API URLs are now determined automatically by the router.
urlpatterns = [
   path("kakao/", views.kakao_login, name="kakao_login"),
    path("kakao/login/", views.kakao_callback, name="kakao_callback"),
    path(
        "kakao/login/finish/",
        views.KakaoLoginView.as_view(),
        name="kakao_login_todjango",
    ),
    path("update/", views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("user/me", views.GetUserInfoView.as_view(), name="get_user_info"),
]