from django.urls import path, include
from accounts import views
#from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
# router = DefaultRouter()

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("kakao", views.kakao_login, name="kakao_login"),
    path(
        "kakao/login",
        views.KakaoLoginView.as_view(),
        name="kakao_login_todjango",
    ),
    path("",include('allauth.urls') ),
    path("update", views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("user/me", views.GetUserInfoView.as_view(), name="get_user_info"),
    path("events/list", views.EventListView.as_view(), name="event_list"),
    path('mypage/', views.MyPageView.as_view(), name='my_page'),  # GET, PUT 요청 처리
]
