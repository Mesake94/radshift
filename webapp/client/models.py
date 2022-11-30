from django.db import models
from django.contrib.auth.models import User
from django_freeradius.models import RadiusCheck
from django.utils import timezone
import random
import string

# Create your models here.
'''
from django.db import models
from django_freeradius.models import RadiusAccounting
from django_freeradius.models import RadiusCheck
from django_freeradius.models import RadiusGroup
from django_freeradius.models import RadiusGroupCheck
from django_freeradius.models import RadiusGroupReply


# RADOP_REPLY_TYPES = (('=', '='),
#                      (':=', ':='),
#                      ('+=', '+='))

# RADCHECK_ATTRIBUTE_TYPES = ['Max-Daily-Session',
#                             'Max-All-Session',
#                             'Max-Daily-Session-Traffic']

# RADCHECK_PASSWD_TYPE = ['Cleartext-Password',
#                         'NT-Password',
#                         'LM-Password',
#                         'MD5-Password',
#                         'SMD5-Password',
#                         'SHA-Password',
#                         'SSHA-Password',
#                         'Crypt-Password']

'''

# the model is used to abstract the freeradius check
# it will map the data volume to proper customer
class SubscriptionPlans(models.Model):

    '''
        Two types of subscription plans
        -> Daily: Fixed volume of data that renews daily
        -> One-Time: Fixed volume of data with fixed expiry date and not renewed upon expiry or data
        depletion
    '''

    plan_type_choices = (
        ('Daily', 'Daily'),
        ('One-Time', 'One-Time'),
    )

    plan_name = models.CharField(max_length=30, unique=True)
    plan_type = models.CharField(max_length=30, choices=plan_type_choices, default='One-Time')
    qouta = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.plan_name}-{self.qouta} MB"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlans, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # rad_check = models.ForeignKey(RadiusCheck, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.user.username}-{self.subscription.plan_name}"

    def data_qouta(self):
        return self.subscription.qouta


class LoginVoucher(models.Model): # this model is used to generate login vouchers
    
    voucher = models.CharField(max_length=30, unique=True, null=True, blank=True)
    mac_address = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subscription = models.ForeignKey(SubscriptionPlans, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



    


