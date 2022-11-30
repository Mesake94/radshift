from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import UserSubscription, LoginVoucher
from django.utils import timezone
from django_freeradius.models import RadiusCheck
import random
import string


def configure_user_subscription(sender, instance, created, **kwargs):
    """_summary_: when a user subscription is created, create a radius check for the user

    Args:
        sender (model): The UserSubscription model
        instance (object): The UserSubscription object
        created (Bool): True if the object is created, False if the object is updated
    """

    if created==True: # only create radius check if the object is created
        # calculate the expiry date
        # if the subscription is daily, the expiry date will be the next day
        if instance.subscription.plan_type == 'Daily':
            instance.expiry_date = timezone.now() + timezone.timedelta(days=1)

        # if the subscription is one-time, the expiry date will be the date specified in the subscription plan
        elif instance.subscription.plan_type == 'One-Time':
            instance.expiry_date = instance.subscription.expiry
        
        instance.save()

        # create radius check for user credentials
        RadiusCheck.objects.create(
            username=instance.user.username,
            value=instance.subscription.qouta,
            op=":=",
            attribute="Max-Daily-Session-Traffic",
            user=instance.user,
            valid_until=instance.expiry_date
        )

# signal for user subscription delete
def delete_user_subscription(sender, instance, **kwargs):

    # delete radius check
    RadiusCheck.objects.filter(username=instance.user.username).delete()


def configure_voucher(sender, instance, created, **kwargs):
    if created==True:
        # generate a random voucher
        voucher = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        instance.voucher = voucher
        # create temporary user for the voucher
        user = User.objects.create_user(username=instance.voucher, password=instance.voucher)
        
        instance.user = user
        # create radius check for user credentials of type Cleartext-Password
        RadiusCheck.objects.create(
            username=instance.user.username,
            value=voucher,
            op=":=",
            attribute="Cleartext-Password",
            user=instance.user,
        )

        # calculate the expiry date
        # if the subscription is daily, the expiry date will be the next day
        if instance.subscription.plan_type == 'Daily':
            instance.expiry_date = timezone.now() + timezone.timedelta(days=1)
        # if the subscription is one-time, the expiry date will be the date specified in the subscription plan
        elif instance.subscription.plan_type == 'One-Time':
            instance.expiry_date = instance.subscription.expiry 

        # create radius check for user credentials
        RadiusCheck.objects.create(
            username=instance.user.username,
            value=instance.subscription.qouta,
            op=":=",
            attribute="Max-Daily-Session-Traffic",
            user=instance.user,
            valid_until=instance.expiry_date,
        )

        instance.save()

# signal for voucher delete
def delete_voucher(sender, instance, **kwargs):
    instance.user.delete()
    # delete radius check
    RadiusCheck.objects.filter(username=instance.user.username).delete()


post_save.connect(configure_user_subscription, sender=UserSubscription)
post_save.connect(configure_voucher, sender=LoginVoucher)
post_delete.connect(delete_voucher, sender=LoginVoucher)
post_delete.connect(delete_user_subscription, sender=UserSubscription)



