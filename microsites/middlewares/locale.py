# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import activate

class LocaleMiddleware(object):
    """ Handles the request for forcing language """

    def process_request(self, request):
        if request.GET.get('locale', None) in dict(settings.LANGUAGES).keys():
            activate(request.GET['locale'])
        