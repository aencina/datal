from django import template
from django.template.loader import render_to_string
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag
def microsite_header(preferences, context_path=None):
    header_uri = preferences['account_header_uri']
    header_height = preferences['account_header_height']
    if header_uri and header_height:
        header_uri += "?locale=%s" % get_language()
        if context_path:
            header_uri += "&page_type=%s" % context_path
        return '<iframe src="'+header_uri+'" style="width:100%;height:'+header_height+'px;border:0;overflow:hidden;" frameborder="0" scrolling="no"></iframe>'
    elif preferences['branding_header']:
        return preferences['branding_header']
    else:
        return render_to_string('css_branding/automatic_header.html', locals())



@register.simple_tag
def microsite_footer(preferences, context_path=None):
    footer_uri = preferences['account_footer_uri']
    footer_height = preferences['account_footer_height']
    if footer_uri and footer_height:
        footer_uri += "?locale=%s" % get_language()
        if context_path:
            footer_uri += "&page_type=%s" % context_path
        return '<iframe src="'+footer_uri+'" style="width:100%;height:'+footer_height+'px;border:0;overflow:hidden;" frameborder="0" scrolling="no"></iframe>'
    else:
        return preferences['branding_footer']


@register.filter(name='replacetext', arg="")
def replacetext(value, arg=''):
    # no cover porque se usa en un plugin deberia estar alla
    vals = arg.split("|") # pragma: no cover
    return value.replace(vals[0], vals[1]) # pragma: no cover


