from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_freeradius.models import RadiusCheck
from passlib.hash import sha512_crypt
from .models import SubscriptionPlans, UserSubscription, LoginVoucher
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",  "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        clear_text_password = self.cleaned_data['password1']
        
        if commit:
            user.save()

        # create radius check for user credentials
        RadiusCheck.objects.create(
            username=user.username,
            # value=sha512_crypt.encrypt(clear_text_password),
            value=clear_text_password,
            op=":=",
            # attribute="Crypt-Password",
            attribute="Cleartext-Password",
            user=user
        )

        return user

class SubscriptionPlansForm(ModelForm):

    class Meta:
        model = SubscriptionPlans
        fields = "__all__"

        # set widgets
        widgets = {
            'qouta': forms.TextInput(attrs={'class': 'form-control', 'type':'number', 'placeholder':'Enter qouta in MB', 'min':'1'}),
            'expiry': forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
        }
        
        def save(self, commit=True):
            plan = super(SubscriptionPlansForm, self).save(commit=False)
            
            if commit:
                plan.save()
            return plan

class UserSubscriptionForm(ModelForm):

    class Meta:
        model = UserSubscription
        fields = ["user", "subscription"]
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'subscription': forms.Select(attrs={'class': 'form-control'}),
        }

        def save(self, commit=True):
            subscription = super(UserSubscriptionForm, self).save(commit=False)
            # subscription.expiry = timezone.now() + timezone.timedelta(days=subscription.plan.expiry)
            if commit:
                subscription.save()
                
            return subscription

class VoucherForm(forms.Form):
    
    plan = forms.ModelChoiceField(queryset=SubscriptionPlans.objects.all(), help_text='Select a subscription', widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'number', 'placeholder':'Enter quantity', 'min':'1'}))

    def save(self, commit=True):
        if commit:
            plan = self.cleaned_data['plan']
            quantity = self.cleaned_data['quantity']
            vouchers = [LoginVoucher(subscription=plan) for _ in range(quantity)]
            for voucher in vouchers: # bulk create will not trigger the post_save signal so we have to call save() on each object
                voucher.save()
            # LoginVoucher.objects.bulk_create(vouchers)       
    

    
    

