from django.http import HttpResponseBadRequest

# decorator function to check if request is htmx
def htmx_required(view_func):
    def _wrapped_view(*args, **kwargs):
    
        if args[1].META.get('HTTP_HX_REQUEST') == 'true':
            return view_func(*args, **kwargs)
        else:
            return HttpResponseBadRequest('This view is only accessible via htmx')
    return _wrapped_view