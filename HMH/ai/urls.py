from django.urls import path
from . import views
from .views import EventImageTestView, GenerateImageView

urlpatterns = [
    path('test/', EventImageTestView.as_view(), name='test'),
    path('generate-image/', GenerateImageView.as_view(), name='generate-image'),
    #path('save-image/', SaveImageView.as_view(), name='save-image'),
]