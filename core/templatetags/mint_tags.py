# -*- coding: utf-8 -*-
from django import template
from django.utils.timezone import now

from datetime import datetime, date
import re
import logging

register = template.Library()


@register.filter(name='datefy')
def datefy(value, arg="%Y-%m-%d"):
    dat = ""
    if type(value) == str:
        try:
            dat = datetime.strptime(value, arg).date()
        except ValueError: #it's not a date
            dat = ""
    elif type(value) == datetime:
        dat = value.strftime(arg)
    return dat


#@register.filter(name='monefy', arg="")
#def monefy(value, arg=''):
#    strformat="#,###.##"
#    strlocale="en_US"
#    currency="USD"
#    vals = arg.split("|")
#    count = 0
#    for val in vals:
#        if count == 0 and val != "":
#            strformat = val
#        if count == 1 and val != "":
#            strlocale = val
#        if count == 2 and val != "":
#            currency = val
#
#        count = count + 1
#
#    value = format_number_ms(value, strformat, strlocale, currency)
#    return value


#@register.filter(name='numberfy', arg="")
#def numberfy(value, arg=''):
#    """
#    it's the same on moneyfy but last paramater "currency" is empty
#    """
#    strformat="#,###.##"
#    strlocale="en_US"
#
#    vals = arg.split("|")
#    count = 0
#    for val in vals:
#        if count == 0 and val != "":
#            strformat = val
#        if count == 1 and val != "":
#            strlocale = val
#
#        count = count + 1
#    try:
#        value = format_number_ms(value, strformat, strlocale, "")
#    except ValueError:
#        value = 0
#    return value


@register.filter(name='isMoney')
def isMoney(value):
    # TODO try to detect better, maybe loading internal "data_source" database field
    return value.find("$") and unicode(value).isnumeric()


@register.filter(name='isNumber')
def isNumber(value):
    if not unicode(value).isnumeric():
        try:
            f = float(value)
        except ValueError:
            return False

    return True


@register.filter(name='extractUrl')
def extractUrl(value):
    return re.search("(?P<url>https?://[^\s]+)", value).group("url")


@register.filter(name='isDate')
def isDate(value):
    res = False
    if type(value) == date:
        res = True
    elif value != "":
        from dateutil.parser import *
        try:
            p = parse(value)
            res = True
        except:
            res = False
    return res


@register.filter(name='jreplace', arg="")
def jreplace(value, arg):
    vals = arg.split("|")
    if type(value) != str and type(value) != unicode: # fail on integer and float
        value = str(value)
        
    ret = value.replace(vals[0], vals[1])    
    return ret

# ---------------------- GRAVES
# import re
import unicodedata


@register.filter(name='urify')
def urify(value):
    v = value.lower()
    rx = re.compile('([/\.;:,\s\(\)])')
    v = unicodedata.normalize('NFKD', v).encode('ascii', 'ignore')
    return rx.sub('_', v)


@register.filter(name='moneyfy')
def moneyfy(value):
    value = str(value)
    v = value.replace('$', '').strip().lower()
    rx = re.compile('([\.,])')
    return rx.sub('', v)


@register.filter(name='money')
def money(value):
    rx = re.compile('^\s*\$?\s*\d{1,3}([,]?\d{3}){0,}([.]\d+){1}$')
    v = value.strip()
    return rx.match(v)


@register.filter(name='dateify', arg="")
def dateify(value, format="%d/%m/%Y"):
    v = value.strip()
    return datetime.strptime(v, format)


@register.filter(name='date', arg="")
def date(value, format="%d/%m/%Y"):
    v = value.strip()
    try:
        datetime.strptime(v, format)
    except:
        return False
    return True


@register.filter(name='strip')
def strip(value):
    return value.strip()

@register.assignment_tag(name='set_value')
def set_value(value):
    return value

@register.assignment_tag(name='add_value', takes_context=True)
def add_value(context, value, addvalue):
    val = context[value]
    orig = [val, addvalue]
    errors = False
    error_log = ''
    if not addvalue:
        addvalue = 0
    if type(val) == str or type(val) == unicode:        
        try:
            val = float(val)
        except:
            errors = True
            error_log = 'Error parsing context value'
            val = 0
            
    if type(addvalue) == str or type(addvalue) == unicode:
        try:
            addvalue = float(addvalue)
        except:
            errors = True
            error_log = 'Error parsing added value'
            addvalue = 0

    if errors:
        logger = logging.getLogger(__name__)
        err_detail = u'WITH ERRORS: {} => ({} + {})'.format(error_log, orig[0], orig[1])
        logger.info(err_detail)
        res = context[value] # return unmodified files
    else:
        res = val + addvalue
    
        
    return res
    
@register.filter(name='exist_day')
def exist_day(arg):        
    vals = arg.split("|")
    day = int(vals[0])
    month = int(vals[1])
    if len(vals) > 2:
        year = int(vals[2])
    else:
        year = now().year + 1 

    try:
        d = date(year, month, day)
        res = True
        details = d.strftime("%d/%m/%y")
    except Exception, e:
        details = 'NO: %d %d %d [%s]' % (year, month, day, str(e))
        res = False

    return res

@register.filter(name='has_31')
def has_31(month):
    if type(month) == str or type(month) == unicode: month = int(month)
    res = month in [1, 3, 5, 7, 8, 10, 12]
    return res

@register.simple_tag(name='my_dict_add', takes_context=True)
def my_dict_add(context, dict_name, idx, val_to_add):
    """ dict of numeric values """
    logger = logging.getLogger(__name__)
    if not context.get(dict_name, None):
        context[dict_name]={}

    errors = False        
    if type(val_to_add) != float:        
        try:
            val_to_add = float(val_to_add)
        except:
            errors = True
            error_log = 'Error parsing context value'
            val_to_add = 0.0

    if errors:    
        err_detail = 'TPL WITH ERRORS: %s => %s - %s - %s' % (error_log, dict_name, idx, str(val_to_add))
        logger.error(err_detail)
    else:            
        if not context[dict_name].get(idx, None): # create if not exists
            context[dict_name][idx] = val_to_add
        else:
            context[dict_name][idx] = context[dict_name][idx] + val_to_add

    return ''