from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .forms import UserForm, ClientDataSubscriptionForm
from django.contrib import messages
from django.contrib.auth.models import User
from django_freeradius.models import RadiusCheck

# Create your views here.
class IndexView(TemplateView):
    template_name = 'demo/index.html'

    def get(self, request):

        return render(request, self.template_name, {})

class UserRegistrationView(TemplateView):
    template_name = 'demo/user_registration.html'
    clients = User.objects.all()

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form':form, 'clients':self.clients})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Registration Successful')
            return render(request, self.template_name, {'form':form, 'clients':self.clients})
        
        return render(request, self.template_name, {'form':form})

# class UserSessionsView(ListView):
#     model = RadiusCheck
#     template_name = 'demo/user_sessions.html'
#     context_object_name = 'sessions'

#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         return RadiusCheck.objects.filter(username=user_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_id'] = self.kwargs['user_id']
#         return context
    
#     def get(self, request):
#         return render(request, self.template_name, {})
class UserSessionsView(TemplateView):
    template_name = 'demo/user_sessions.html'
    clients = User.objects.all()

    def get(self, request):
        form = ClientDataSubscriptionForm()
        return render(request, self.template_name, {'clients':self.clients, 'form':form})

    def post(self, request):
        form = ClientDataSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client Data Subscription Successful')
            return render(request, self.template_name, {'clients':self.clients, 'form':form})
        # sessions = RadiusCheck.objects.filter(username=user_id)
        return render(request, self.template_name, {'clients':self.clients, 'form':form})
    


    


