from client.models import UserSubscription
from django.contrib.auth.models import User
from django_freeradius.models import RadiusAccounting
import subprocess
import os
from django.utils import timezone

def forcefully_disconnect_user(session_id):
    """
    The function will make a radius disconnect request to the NAS
    to forcefully disconnec the user
    """

    # get the accounting session based on id
    accounting_session = RadiusAccounting.objects.get(id=session_id)
    
    # construct the radius packet
    radius_packet = f"""
User-Name = "{accounting_session.username}"
User-Password = "Testing123!"
NAS-IP-Address = 192.168.1.101
Calling-Station-Id = {accounting_session.calling_station_id}
    """
    
    # # write the radius packet to a txt file
    # with open('disconnect_packet.txt', 'w') as f:
    #     f.write(radius_packet)

    # execute the .sh script to send the radius packet and get the response
    # response = subprocess.check_output(['/home/mess/Projects/RadiusServer/radclient-testing/run.sh'])
    # print(response)
    subprocess.Popen(['sh', '/home/mess/Projects/RadiusServer/radclient-testing/run.sh'])
    # subprocess.call(['/home/mess/Projects/RadiusServer/webapp/client/disconnect_user.sh'])

class SubscriptionUsage:
    """
        The class is a wrapper for the UserSubscription model and adds
        functionality to get the usage of the subscription 
    """
    octets_ratio = 300/3000000000 # Megabytes/octets
    
    def __init__(self, subscription: UserSubscription=None):
        self.subscription = subscription
    
    def deactivate(self):
        """
            The function will deactivate the subscription
        """
        self.subscription.is_active = False
        self.subscription.save()
        print(f"[+] Deactivated subscription {self.subscription.subscription.plan_name}..")

    def is_expired(self):
        """
            The function will check if the subscription has expired
        """
        return self.subscription.expiry_date < timezone.now()
        
    
class UserMonitoringModule:

    octets_ratio = 300/3000000000 # Megabytes/octets

    def __init__(self, client:User):
        """The class collects the session info for the client and computes
        the total amount of data used by the client

        Args:
            client (User): the client to monitor
        """
        self.client = client

    def get_user_subscriptions(self):
        """
        The function returns the user's active subscriptions. A user may be subscribed to multiple
        subscriptions. The queryset is ordered by the date the subscription was created. The first
        subscription is the most earliest subscription.
        """
        return UserSubscription.objects.filter(user=self.client, is_active=True).order_by('created_at')

    def disconnect_user(self):
        print("[+] Disconnecting user..")

    def manage_subscriptions(self):
        """
        The function manages the users subscriptions. If the user has exceeded the quota for the
        subscription, the subscription will be deactivated and the user will be disconnected from the
        network. For multiple subscriptions, the function will deactivate the subscription that was
        created first. If the subscription has expired, the function will deactivate the subscription.
        If the subscription is the last subscription, the function will deactivate the subscription and
        disconnect the user from the network. 
        """

        # get the user's active subscriptions
        active_subscriptions = self.get_user_subscriptions()

        # if the user has no active subscriptions, disconnect the user
        if not active_subscriptions:
            self.disconnect_user()
            return

        # loop through the subscriptions and check if the subscription has expired or if the user has exceeded the quota
        _active_subscriptions = [SubscriptionUsage(subscription) for subscription in active_subscriptions]
        for subscription in _active_subscriptions:
            if subscription.is_expired(): # deactivate the subscription if it has expired
                subscription.deactivate()
            elif self.get_total_usage() >= subscription.subscription.qouta:
                # deactivate the subscription if the user has exceeded the quota
                # subscriptions are deactivated in the order of their expiry date
                # the subscriptions that expire first are deactivated first
                subscription.deactivate()
            
    @property
    def accounting_data(self):
        """The accounting data for each user session has a unique session id. The calling-session-id is also unique across devices which may use the same login credentials.

        Pull the accounting data for each user and group them by session id. This will give us the total data used by each session.

        Returns:
            Object: The accounting data grouped by session id
        """
        
        accounting_data = RadiusAccounting.objects.filter(username=self.client.username)
        
        # get distinct session ids from the accounting data
        unique_session_ids = []
        for data in accounting_data:
            if data.calling_station_id not in unique_session_ids:
                unique_session_ids.append(data.calling_station_id)

        # group the accounting data by session id and return it
        return {session_id: accounting_data.filter(calling_station_id=session_id) for session_id in unique_session_ids}

    @property
    def total_octets_upload(self):
        """Get the total octets uploaded by the user

        Returns:
            int: The total octets uploaded by the user
        """
        total_octets = 0
        for session_id, session_data in self.accounting_data.items():
            for data in session_data:
                total_octets += data.input_octets
        
        return total_octets

    @property
    def total_octets_download(self):
        """Get the total octets downloaded by the user

        Returns:
            int: The total octets downloaded by the user
        """
        total_octets = 0
        for session_id, session_data in self.accounting_data.items():
            for data in session_data:
                total_octets += data.output_octets

        return total_octets

    @property
    def total_octets(self):
        """Get the total octets used by the user

        Returns:
            int: The total octets used by the user
        """
        return self.total_octets_upload + self.total_octets_download

    @property
    def total_megabytes(self):
        """Get the total megabytes used by the user

        Returns:
            int: The total megabytes used by the user
        """
        return self.total_octets * self.octets_ratio

    @property
    def total_qouta(self):
        """Get the total qouta for the user

        Returns:
            int: The total qouta for the user
        """
        return sum(subscription.subscription.qouta for subscription in self.get_user_subscriptions()) or 0.0

    @property
    def has_exceeded_quota(self):
        """Check if the user has exceeded the quota

        Returns:
            bool: True if the user has exceeded the quota, False otherwise
        """
        
        # print(self.get_user_subscriptions().last())
        return self.total_megabytes > self.total_qouta
    
    @property
    def latest_session(self):
        """Get the latest session for the user

        Returns:
            Object: The latest session for the user
        """
        return RadiusAccounting.objects.filter(username=self.client.username).latest('start_time')
    
    def get_total_usage(self):
        """Get the total usage for the user

        Returns:
            int: The total usage for the user
        """
        return self.total_megabytes



    