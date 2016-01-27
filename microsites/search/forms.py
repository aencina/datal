from django import forms
from django.conf import settings
from django.utils.html import escape as html_escape


class SearchForm(forms.Form):
    q = forms.CharField(label='Query', max_length=512, required=False)
    page = forms.IntegerField(label='Page', required=False)
    tag = forms.RegexField(label='Tag', required=False, regex = r'[a-zA-Z0-9]+')
    order = forms.CharField(label='Order', required=False)
    reverse = forms.CharField(label='Reverse', required=False)

    def clean_page(self):
        # default page
        page = self.cleaned_data['page']
        if not page:
            return 1
        page = abs(page)
        if page > settings.SEARCH_MAX_RESULTS / settings.PAGINATION_RESULTS_PER_PAGE:
            raise forms.ValidationError("Max page number")
        return page

    def clean_q(self):
        self.cleaned_data['q']=self._escape()
        return self.cleaned_data['q'].strip()

    def clean_tag(self):
        return self.cleaned_data['tag'].strip()

    def clean_reverse(self):
        return self.cleaned_data['reverse'].strip()

    def _escape(self):
        """metodo que devuelve el q limpio de caracteres especiales"""

        # eliminamos los chars especiales
        # https://lucene.apache.org/core/2_9_4/queryparsersyntax.html#Escaping%20Special%20Characters
        map(self._replace, ("+","-","&&","||","!","(",")","{","}","[","]","^","\"","~","*","?",":","\\", "/"))

        return html_escape(self.cleaned_data['q'])

    def _replace(self, r):
        """devuelve q sin el char r"""
        self.cleaned_data['q']=self.cleaned_data['q'].replace(r, "")

    def get_query(self):
        query = self.cleaned_data['q']
        query = query and query or self.cleaned_data['tag']

        # your code is now here
        if not query:
            query = u'%'

        return query
