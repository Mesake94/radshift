from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import requests
from django.contrib.auth.models import User
from django_freeradius.models import RadiusCheck
from passlib.hash import sha512_crypt

# Create your views here.
class CaptivePortalView(TemplateView):

    template_name = 'captiveportal/login.html'

    def get(self, request):
        ga_ssid = request.GET.get('ga_ssid', '')
        ga_ap_mac = request.GET.get('ga_ap_mac', '')
        ga_nas_id = request.GET.get('ga_nas_id', '')
        ga_srvr = request.GET.get('ga_srvr', '')
        ga_cmac = request.GET.get('ga_cmac', '')
        ga_Qv = request.GET.get('ga_Qv', '')
        ga_orig_url = request.GET.get('ga_orig_url')

        # if ga_ssid == '':
        #     return HttpResponse('SSID is required', status=400)
        # if ga_ap_mac == '':
        #     return HttpResponse('AP MAC is required', status=400)
        # if ga_nas_id == '':
        #     return HttpResponse('NAS ID is required', status=400)
        # if ga_srvr == '':
        #     return HttpResponse('SRVR is required', status=400)
        # if ga_cmac == '':
        #     return HttpResponse('CMAC is required', status=400)
        # if ga_Qv == '':
        #     return HttpResponse('QV is required', status=400)
        
        # save the parameters above in the session
        request.session['ga_ssid'] = ga_ssid
        request.session['ga_ap_mac'] = ga_ap_mac
        request.session['ga_nas_id'] = ga_nas_id
        request.session['ga_srvr'] = ga_srvr
        request.session['ga_cmac'] = ga_cmac
        request.session['ga_Qv'] = ga_Qv
        request.session['ga_orig_url'] = ga_orig_url
        
        # persist the session
        request.session.modified = True
        url = f"http://{ga_srvr}:880/cgi-bin/hotspot_login.cgi?ga_ssid={ga_ssid}&ga_ap_mac={ga_ap_mac}&ga_nas_id={ga_nas_id}&ga_srvr={ga_srvr}&ga_cmac={ga_cmac}&ga_Qv={ga_Qv}"

        return render(request, self.template_name, {'url':url})

    def post(self, request):
        try:
            ga_user = request.POST.get('ga_user')
            ga_pass = request.POST.get('ga_pass')
            # check if the user exists
            
            user = User.objects.filter(username=ga_user)

            if not user.exists():
                return JsonResponse({'success': 'False', 'message':'User does not exists'}, status=400)

            # check  the radius check attributes
            radius_check = RadiusCheck.objects.filter(username=ga_user, attribute='Cleartext-Password', value=ga_pass)
            
            return JsonResponse({'success': True, 'message': 'Authenticated successfully'}, status=200) if radius_check.exists() else JsonResponse({'success': False, 'message': 'Wifi credentials are invalid'}, status=400)
        except Exception as e:
            return JsonResponse({'success': 'False', 'message': str(e)}, status=400)
        