from allauth.account.views import LogoutView
import accounts
from accounts.views import index

urlpatterns = [

    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    
]