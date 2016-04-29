from django import forms
from django.utils.translation import ugettext_lazy
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from core import choices
from core.models import Role


class AccountInfoForm(forms.Form):
    """La informacion de la cuenta segraba en forma de preferencias
    Estas tienen un campo de tipo TextField sin max_length definido.
    De todas formas cada campo debe tener algun limite"""
    account_name = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-NAME-LABEL'), required=True)
    account_link = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-LINK-LABEL'), required=False)
    account_contact_person_name = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-CONTACT-PERSON-NAME-LABEL'), required=False, max_length=80)
    account_contact_person_email = forms.EmailField(label=ugettext_lazy('ACCOUNT-FORM-CONTACT-PERSON-EMAIL-LABEL'), required=False, max_length=120)
    account_contact_dataperson_email = forms.EmailField(label=ugettext_lazy('ACCOUNT-FORM-CONTACT-DATAPERSON-EMAIL-LABEL'), required=False, max_length=120)
    account_contact_person_phone = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-CONTACT-PERSON-PHONE-LABEL'), required=False, max_length=80)
    account_contact_person_country = forms.ChoiceField(choices=choices.COUNTRY_CHOICES, label=ugettext_lazy('ACCOUNT-FORM-CONTACT-PERSON-COUNTRY-LABEL'), required=False)

    def action(self):
        return reverse('admin_manager.edit_info_update')


class AccountBrandingForm(forms.Form):
    account_page_titles = forms.CharField(label=ugettext_lazy('ACCOUNT-HTML-TITLE-LABEL'), required=False)
    account_header_uri = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-HEADER-URI-LABEL'), required=False)
    account_header_height = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-HEIGHT-LABEL'), required=False)
    account_footer_uri = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-FOOTER-URI-LABEL'), required=False)
    account_footer_height = forms.CharField(label=ugettext_lazy('ACCOUNT-FORM-HEIGHT-LABEL'), required=False)
    account_favicon = forms.FileField(label=ugettext_lazy('ACCOUNT-FORM-FAVICON-LABEL'), required=False)
    account_logo = forms.FileField(label=ugettext_lazy('ACCOUNT-FORM-LOGO-LABEL'), required=False)

    account_title_color = forms.CharField(label=ugettext_lazy('ACCOUNT-TITLE-COLOR'), required=False, widget=forms.HiddenInput())
    account_button_bg_color = forms.CharField(label=ugettext_lazy('ACCOUNT-BG-COLOR'), required=False, widget=forms.HiddenInput())
    account_button_border_color = forms.CharField(label=ugettext_lazy('ACCOUNT-BORDER-COLOR'), required=False, widget=forms.HiddenInput())
    account_button_font_color = forms.CharField(label=ugettext_lazy('ACCOUNT-FONT-COLOR'), required=False, widget=forms.HiddenInput())
    account_mouseover_bg_color = forms.CharField(label=ugettext_lazy('ACCOUNT-BG-COLOR'), required=False, widget=forms.HiddenInput())
    account_mouseover_border_color = forms.CharField(label=ugettext_lazy('ACCOUNT-BORDER-COLOR'), required=False, widget=forms.HiddenInput())
    account_mouseover_title_color = forms.CharField(label=ugettext_lazy('ACCOUNT-TITLE-COLOR'), required=False, widget=forms.HiddenInput())
    account_mouseover_text_color = forms.CharField(label=ugettext_lazy('ACCOUNT-TEXT-COLOR'), required=False, widget=forms.HiddenInput())

    account_header_bg_color = forms.CharField(label=ugettext_lazy('ACCOUNT-BG-COLOR'), required=False, widget=forms.HiddenInput())
    account_header_border_color = forms.CharField(label=ugettext_lazy('ACCOUNT-BORDER-COLOR'), required=False, widget=forms.HiddenInput())

    def action(self):
        return reverse('admin_manager.edit_branding_update')


class AccountSocialForm(forms.Form):
    account_comments = forms.BooleanField(label=ugettext_lazy('ACCOUNT-ENABLE-COMMENTS-LABEL'), required=False)
    enable_embed_options = forms.BooleanField(label=ugettext_lazy('ACCOUNT-ENABLE-EMBED-OPTIONS-LABEL'), required=False)
    account_enable_sharing = forms.BooleanField(label=ugettext_lazy('ACCOUNT-ENABLE-SHARING-LABEL'), required=False)
    account_enable_notes = forms.BooleanField(label=ugettext_lazy('ACCOUNT-ENABLE-NOTES-LABEL'), required=False)
    account_dataset_download = forms.BooleanField(label=ugettext_lazy('ACCOUNT-ENABLE-DOWNLOADS-LABEL'), required=False)
    account_dataset_show = forms.BooleanField(label=ugettext_lazy('ACCOUNT-ENABLE-DATASET-SHOW-LABEL'), required=False)

    def action(self):
        return reverse('admin_manager.edit_social_update')


class AccountDomainForm(forms.Form):
    account_domain = forms.CharField(required=True, widget=forms.HiddenInput())
    account_domain_internal = forms.CharField(label=ugettext_lazy('ACCOUNT-DOMAIN-LABEL'), required=False)
    account_domain_external = forms.CharField(label=ugettext_lazy('ACCOUNT-DOMAIN-EXTERNAL-LABEL'), required=False)
    account_api_domain = forms.CharField(required=True, widget=forms.HiddenInput())
    account_transparency_domain = forms.CharField(label=ugettext_lazy('ACCOUNT-DOMAIN-TRANSPARENCY-LABEL'), required=False, widget=forms.HiddenInput())

    pick_a_domain = forms.ChoiceField(choices=(('internal', 'internal'),('external', 'external')), required=True, widget=forms.RadioSelect())

    def action(self):
        return reverse('admin_manager.edit_domain_update')


class CategoryCreateForm(forms.Form):
    name = forms.CharField(label=ugettext_lazy('WORKSPACE-CATEGORY-NAME-LABEL'), required=True, max_length=45)
    description = forms.CharField(label=ugettext_lazy('WORKSPACE-CATEGORY-DESCRIPTION-LABEL'), required=False, widget=forms.Textarea(), max_length=140)
    is_default = forms.BooleanField(label=ugettext_lazy('ACCOUNT-DEFAULT-CATEGORY-LABEL'), required=False)


class CategoryEditForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    name = forms.CharField(label=ugettext_lazy('APP-NAME-TEXT'), required=True, max_length=45)
    description = forms.CharField(label=ugettext_lazy('APP-DESCRIPTION-TEXT'), required=False, widget=forms.Textarea())
    is_default = forms.BooleanField(label=ugettext_lazy('ACCOUNT-DEFAULT-CATEGORY-LABEL'), required=False)


class CategoryDeleteForm(forms.Form):
    id = forms.IntegerField(required=True)


class UserForm(forms.Form):

    # Patch, deberiamos usa run model i18n
    def translateRole(self, code):
        if code == 'ao-account-admin':
            return ugettext_lazy('APP-TEXT-ADMIN')
        elif code == 'ao-editor':
            return ugettext_lazy('APP-TEXT-COLLECTOR')
        elif code == 'ao-publisher':
            return ugettext_lazy('APP-TEXT-PUBLISHER')
        else:
            return ugettext_lazy('APP-TEXT-COLLECTOR')


    def __init__(self, role_codes, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        roles = Role.objects.values('name', 'code').filter(code__in = role_codes).all().order_by('-id')
        role_choices = []
        for role in roles:
            role_choices.append((role['code'],self.translateRole(role['code'])))
        role_choices = tuple(role_choices)
        self.fields['role'] = forms.ChoiceField(label=ugettext_lazy('APP-ROLE-TEXT'), required=True, choices = role_choices)

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(label=ugettext_lazy('APP-NAME-TEXT'), required=True)
    username = forms.CharField(label=ugettext_lazy('APP-USERNAME-TEXT'), required=True)
    email = forms.CharField(label=ugettext_lazy('APP-EMAIL-TEXT'), required=True, validators=[validate_email])
    confirm_email = forms.CharField(label=ugettext_lazy('APP-CONFIRMEMAIL-TEXT'), required=True, validators=[validate_email])

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email != confirm_email:
            raise forms.ValidationError(ugettext_lazy('APP-EMAILS-MUST-MATCH'))

        return cleaned_data


class UserDeleteForm(forms.Form):
    id = forms.IntegerField(required=True)
