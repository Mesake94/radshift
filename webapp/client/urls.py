from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('RegistrationAPI/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('SubscriptionsPlanAPI/', views.SubscriptionPlansView.as_view(), name='subscription-plans'),
    path('UserSubscriptionAPI/', views.UserSubscriptionView.as_view(), name='user-subscription'),
    path('UserMonitoringAPI/', views.UserMonitoringView.as_view(), name='user-monitoring'),
    path('VoucherAPI/', views.VoucherManagement.as_view(), name='voucher-management'),
]