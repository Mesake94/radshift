'''
    The file contains code that runs in the background and used for monitoring the user's usage.
    The code is run in a separate thread to prevent being blocked. If the server is restarted, the code will be run again.
    It is triggered by the ready() function in webapp/client/apps.py
'''
import threading
from django_freeradius.models import RadiusAccounting
from time import sleep
from ..modules.monitoring import UserMonitoringModule
from ..models import UserSubscription
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class BackgroundUserMonitor(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        
    def run(self):
        # sleep for 10 seconds to allow the server to start
        sleep(10)
        while True:
            try:
                # get all active subscriptions
                active_subscriptions = UserSubscription.objects.filter(is_active=True)

                for subscription in active_subscriptions:
                    usage_monitor = UserMonitoringModule(client=subscription.user).manage_subscriptions()
                    
                sleep(10)
            except Exception as e:
                print(f"** An exception occured: {e} **")
                # sleep for 30 seconds before trying again
                sleep(30)
            except KeyboardInterrupt:
                # close the thread
                print('** Closing the thread **')
                ## remove the thread from the thread list
                threading.enumerate().remove(self)
                break






