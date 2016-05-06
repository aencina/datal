# -*- coding: utf-8 -*-
import logging
import json
from uuid import uuid4

from rdflib import Literal, URIRef, Graph, XSD

from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter(is_safe=True)
def literal(value='', arg=None):
	"""
	Returns a literal version of a string, espcaed and doble quoted
	"""
	if arg:
		serial = u'{}'.format(Literal(value, datatype=XSD[arg]).n3())
	else:
		serial = u'{}'.format(Literal(value).n3())
	return mark_safe(serial)

@register.filter(is_safe=True)
def uuid(value):
	"""
	Returns an unicode string version of a uuid4
	"""
	string = unicode(value)+"-"+unicode(uuid4())
	return mark_safe(string)

@register.assignment_tag(name='equals')
def equals(val1, val2):
    return val1 == val2
