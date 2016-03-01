from core import VERSION


def request_context(request):
    obj = {'core_version': VERSION}
    return obj
