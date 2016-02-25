from django.conf import settings
from core import VERSION

def request_context(request):
    obj = {}
    obj['core_version']=VERSION
    return obj
