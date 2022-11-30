from django.urls import path
from . import views

urlpatterns = [
    path('', views.CaptivePortalView.as_view(), name='captive-portal'),
]


