from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext

class PrivateDataStreamShareForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput)

    def action(self):
        return reverse('auth.grant_datastream')

class CollaboratorForm(forms.Form):
    nick = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True, widget=forms.HiddenInput)
    role = forms.ChoiceField(required=True, choices=(('ao-viewer', ugettext('OVPRIV-CANVIEW-TEXT')),
                                                     ('ao-user', ugettext('OVPRIV-CANUSE-TEXT'))),
                                                     widget=forms.Select(attrs={'class':'FR selectField'})
                                                     )

class PrivateVisualizationShareForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput)

    def action(self):
        return reverse('auth.grant_visualization')

class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
