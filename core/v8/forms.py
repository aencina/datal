# -*- coding: utf-8 -*-

import re

from django import forms
from django.forms.formsets import BaseFormSet
from core.primitives import PrimitiveComputer
from core.v8.commands import *

class DefaultForm(forms.Form):
    def clean(self):
        cleaned_data = super(DefaultForm, self).clean()
        for field in self:
            if (field.field.initial and (field.name not in cleaned_data or 
                                         not cleaned_data[field.name])):
                cleaned_data[field.name] = field.field.initial
       
        return cleaned_data

class ArgumentForm(forms.Form):
    name=forms.CharField(max_length=16, widget=forms.TextInput(), required=True)
    value=forms.CharField(max_length=100, widget=forms.TextInput(), required=True)

class RequestForm(DefaultForm):
    revision_id = forms.IntegerField(required=True)
    page = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    output=forms.CharField(max_length=100, required=False)
    where= forms.CharField(required=False)
#    passticket = forms.CharField(required=False)
#    if_modified_since = forms.IntegerField(required=False)
#    ttl = forms.IntegerField(required=False)


class DatastreamRequestForm(RequestForm):
    tableid = forms.CharField(required=False)
    # pWhereExpr: Condicion logica para unit los filtros
    whereExpr= forms.CharField(required=False)
    # pIfModified: Fecha y hora en formato unix que usara el motor para comprobar si el datastream se actualizo desde entonces, y en caso contrario devolver un not modified exception.
    ifModified= forms.CharField(required=False)

    # pTableFormat: Objeto en notacion json con el formato a aplicar sobre cada columna del datastream. ver http://wiki.junar.com/index.php/API#Formateo_de_Datos
    format= forms.CharField(required=False)

class UpdateGridRequestForm(RequestForm):
    # pLimit
    rp = forms.IntegerField(required=False)
    # se usa para luego armar un pFilter0
    query = forms.CharField(required=False)

class RequestFormSet(BaseFormSet):
    _is_multi_argument=re.compile("(?P<argument>\D+)(?P<order>\d+)").match
    _is_primitive_argument=re.compile("pArgument(?P<order>\d+)").match

    def __init__(self, *args, **kwargs):
        new_args=[]
        for i,j in enumerate(args):
            aux=dict(j)

            for key in aux.keys():
                aux['form-0-%s' % key]=aux[key]
            aux.update({'form-TOTAL_FORMS': u'1', 'form-INITIAL_FORMS': u'0','form-MAX_NUM_FORMS': u''})
            new_args.append(aux)

        self._defaults=kwargs.get("default",[])

        super(RequestFormSet, self).__init__(*new_args)

    def _update_defaults(self):

        for arg in self._defaults:
            key="pArgument%s" % arg["position"]
            value = self.data.get(key,None)

            if value in (None, ""):
                self.data[key]=arg["default"]
                
    def clean(self):

        if any(self.errors):
            return

        # aplicamos los valores defaults
        self._update_defaults()

        #self.forms=[]
        for key in self.data.keys():
            # evitamos los form-algo
            if key[0:4] == "form":
                continue

            # si es AlgoNN
            if self._is_multi_argument(key):
                try:
                    valor = self.data[key]
                    if self._is_primitive_argument(key):
                        valor =  PrimitiveComputer().compute(self.data[key])
                    f=ArgumentForm({"name": key, 'value':valor})
                    if f.is_valid():
                        self.forms.append(f)
                    else:
                        self.errors.append({key: [u"argumento no válido (%s)", self.data[key]]})
                        raise forms.ValidationError(u"argumento no válido", code="argument_not_valid")
                except TypeError,e:
                    self.errors.append({'value': [u"expected string or buffer (%s)" % e]})
                    raise forms.ValidationError(u"expected string or buffer", code="typeerror")
                
                #no me gusta, debería tener un map y un filter, refactorear vago!
                continue

    def _get_doc_dict(self, doc_type):
        if doc_type in ["datastream_revision", "datastream"]:
            return "ds"
        elif doc_type in ["visualization_revision","visualization"]: 
            return "vz"
        elif doc_type in ["dataset_revision","dataset"]: 
            return "ds"

    def _serialize_data(self, l):
        if l['value']:
            self.cleaned_data_plain.update({l['name']: l['value']})

    def get_cleaned_data_plain(self):
        """Serializa el cleaned_data para el motor"""

        if self.cleaned_data:
            # Obtenemos solo los parametros con valores
            self.cleaned_data_plain = {k: v for k, v in self.cleaned_data[0].items() if v }

            # luego serializamos los forms de argumentos
            map(self._serialize_data, self.cleaned_data[1:])
            
            return self.cleaned_data_plain
            
        return {}
            
