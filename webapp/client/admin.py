from django.contrib import admin
from .models import SubscriptionPlans, UserSubscription, LoginVoucher

# Register your models here.
admin.site.register(SubscriptionPlans)
admin.site.register(UserSubscription)
admin.site.register(LoginVoucher)


