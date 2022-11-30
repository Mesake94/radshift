from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from .decorators import htmx_required
from .forms import UserRegistrationForm, SubscriptionPlansForm, UserSubscriptionForm, VoucherForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import SubscriptionPlans, UserSubscription, LoginVoucher
from .modules.monitoring import UserMonitoringModule, forcefully_disconnect_user

# Create your views here.
class IndexView(TemplateView):

    template_name = 'client/index.html'

    def get(self, request):
        return render(request, self.template_name, {})

class UserRegistrationView(TemplateView):

    template = 'client/user-registration/registration.html'
    clients = User
    @htmx_required
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template, {'form': form, 'users': self.clients.objects.filter(is_active=True, is_staff=False, is_superuser=False)})
    
    @htmx_required
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registration successful')
            
        return render(request, self.template, {'form': form, 'users':self.users})

class SubscriptionPlansView(TemplateView):
    template = 'client/subscription-plans/register.html'
    model = SubscriptionPlans

    def get(self, request):
        form = SubscriptionPlansForm()
        return render(request, self.template, {'form':form, 'plans':self.model.objects.filter(is_active=True)})

    def post(self, request):
        form = SubscriptionPlansForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription plan registration successful')

        return render(request, self.template, {'form':form, 'plans':self.plans})

# do not cache this view

class UserSubscriptionView(TemplateView):

    template = 'client/user-subscription/register.html'
    user_plans = UserSubscription
    
    @htmx_required
    def get(self, request):
        form = UserSubscriptionForm()
        return render(request, self.template, {'form':form, 'user_plans':self.user_plans.objects.all()})

    @htmx_required
    def post(self, request):
        form = UserSubscriptionForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'User subscription successful')
            else:
                messages.error(request, 'User subscription failed')
        except Exception as exc:
            messages.error(request, f'User subscription failed: {exc}')
        
        return render(request, self.template, {'form':form, 'user_plans':self.user_plans}) 
    
    
class UserMonitoringView(TemplateView):
    template = 'client/user-monitoring/monitor.html'
  
    def get(self, request):
        dataset = [UserMonitoringModule(user) for user in User.objects.all()]
        return render(request, self.template, {'dataset':dataset})

    def post(self, request):
        session_id = request.POST.get('session_id')
        try:
            forcefully_disconnect_user(session_id)
            return HttpResponse('User disconnected successfully..', 201)
        except Exception as exc:
            return HttpResponse(f'Unable to disconnect user..{str(exc)}', 400)


class VoucherManagement(TemplateView):
    template = 'client/voucher-management/register.html'

    def get(self, request):
        form = VoucherForm()
        return render(request, self.template, {'form':form})

    def post(self, request):
        form = VoucherForm(request.POST)
        vouchers = LoginVoucher.objects.all()
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Voucher registration successful')
            else:
                messages.error(request, f'Voucher registration failed. {form.errors}')
        except Exception as exc:
            messages.error(request, f'Voucher registration failed: {exc}')

        return render(request, self.template, {'form':form, 'vouchers':vouchers})

    
        



    