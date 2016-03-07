# -*- coding: utf-8 -*-
import logging
import json
from uuid import uuid4

from rdflib import Literal, URIRef, Graph

from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter(is_safe=True)
def literal(value):
	"""
	Returns a literal version of a string, espcaed and doble quoted
	"""
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