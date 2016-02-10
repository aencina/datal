from django.http import HttpResponseRedirect

def home(request):
    auth_manager = request.auth_manager
    if auth_manager.is_anonymous():
        return HttpResponseRedirect('/signin/')
    else:
        return HttpResponseRedirect('/welcome/')
