
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.IndexView.as_view(), name='index'),
   path('User-Registration/', views.UserRegistrationView.as_view(), name='user-registration'),
   path('User-Sessions/', views.UserSessionsView.as_view(), name='user-sessions'),
]
