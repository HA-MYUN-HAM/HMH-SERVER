from django.urls import path
#from rest_framework.routers import DefaultRouter
from sample_swagger.views import TestView

# Create a router and register our viewsets with it.
# router = DefaultRouter()

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('v1/test/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]