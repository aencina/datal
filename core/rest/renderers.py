from rest_framework import renderers
from rest_framework.renderers import JSONRenderer

class UTF8JSONRenderer(renderers.JSONRenderer):
    charset = 'utf-8'