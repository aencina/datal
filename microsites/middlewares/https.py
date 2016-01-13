from django.conf import settings
from django.http import HttpResponseRedirect

class SSLRedirect(object):
    def request_is_secure(self, request):
        if request.is_secure():
            return True

        # Handle forwarded SSL (used at Webfaction)
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        if 'HTTP_X_SSL_REQUEST' in request.META:
            return request.META['HTTP_X_SSL_REQUEST'] == '1'

        return False

    def _redirect(self, request):
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError(
            """Django can't perform a SSL redirect while maintaining POST data.
                Please structure your views so that redirects only occur during GETs.""")

        newurl = "https://%s%s" % (request.get_host(),request.get_full_path())

        return HttpResponseRedirect(newurl)

    def process_request(self, request):
        if settings.DEBUG:
            return None

        if not self.request_is_secure(request):
            if request.preferences['account.microsite.https']:
                return self._redirect(request)
        else:        
            request.IS_SECURE=True

        return None

        
