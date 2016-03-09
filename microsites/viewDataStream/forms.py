from django import forms
from django.conf import settings

class LegacyEmbedForm(forms.Form):
    dataservice_id = forms.IntegerField(required=True)
    end_point = forms.CharField(required=False)
    header_row = forms.IntegerField(required=False)
    fixed_column = forms.IntegerField(required=False)

class RequestForm(forms.Form):
    datastream_revision_id = forms.IntegerField(required=True)
    limit = forms.IntegerField(required=False)

class SearchForm(forms.Form):
    query       = forms.CharField(required=False)
    max_results = forms.IntegerField(required=False, max_value=100, min_value=1)
    order       = forms.CharField(required=False)

    def clean_max_results(self):
        l_default_max_results = 999
        try:
            max_results = int(self.cleaned_data['max_results'])
            return max_results <= l_default_max_results and max_results or l_default_max_results
        except:
            return l_default_max_results
