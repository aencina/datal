from django.conf import settings
from django.shortcuts import render_to_response as django_render_to_response
from django.template import RequestContext


def render_to_response(template, dictionary, mimetype=settings.DEFAULT_CONTENT_TYPE):
    try:
        request = dictionary.pop('request')
    except:
        request = dictionary
    context_instance = RequestContext(request)
    return django_render_to_response(template, dictionary, context_instance, mimetype=mimetype)
