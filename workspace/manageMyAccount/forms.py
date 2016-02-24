from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from core.models import User
import hashlib
from core import choices


class SignUpForm(forms.Form):
    account_name = forms.CharField(required=True, label=ugettext_lazy('APP-ACCOUNT-NAME-TEXT'), max_length=80)
    admin_url = forms.CharField(required=True, label=ugettext_lazy('APP-ADMIN-URL-TEXT'))
    nick = forms.CharField(required=True, label=ugettext_lazy('APP-USERNICK-TEXT'))
    name = forms.CharField(required=True, label=ugettext_lazy('APP-USERNAME-TEXT'))
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False),
                               label=ugettext_lazy('APP-PASSWORD-TEXT'))
    password_again = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False),
                                     label=ugettext_lazy('UPDATE-PASSWORD-CONFIRMPSW'))
    email = forms.CharField(required=True, label=ugettext_lazy('APP-EMAIL-TEXT'))
    language = forms.ChoiceField(required=True, choices=choices.LANGUAGE_CHOICES,
                                 label=ugettext_lazy('APP-LANGUAGE-TEXT'))

    def action(self):
        return reverse('accounts.create')

    def clean_password(self):
        return hashlib.md5(self.cleaned_data.get('password')).hexdigest()


    def clean_account_name(self):
        # Solo \w+
        if self.cleaned_data['account_name'].isalpha():
            return self.cleaned_data['account_name']
        raise ValidationError(ugettext_lazy('APP-ACCOUNT-NAME-NOT-VALID'))


class SignInForm(forms.Form):
    admin_url = forms.CharField(required=False, widget=forms.HiddenInput())
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))
    remember_me = forms.BooleanField(label=ugettext_lazy('APP-REMEMBERME-TEXT'), required=False)
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def action(self):
        return reverse('accounts.login')

    def clean_password(self):
        return hashlib.md5(self.cleaned_data.get('password')).hexdigest()

    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        try:
            self.user = User.objects.get(nick = username)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

        if self.user.password != password:
            self.user = None
            raise forms.ValidationError("Invalid data")

        return cleaned_data


class ActivateUserForm(forms.Form):
    ticket = forms.CharField(required=True, widget=forms.HiddenInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))
    password_again = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))

    def clean_password(self):
        return hashlib.md5(self.cleaned_data.get('password')).hexdigest()

    def clean_password_again(self):
        return hashlib.md5(self.cleaned_data.get('password_again')).hexdigest()

    def clean(self):
        cleaned_data = super(ActivateUserForm, self).clean()

        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        if password != password_again:
            raise forms.ValidationError(ugettext_lazy('APP-PASSWORD-MUST-MATCH'))

        return cleaned_data

    def action(self):
        return reverse('accounts.activate')


class MyAccountForm(forms.ModelForm):
    old_password = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False),
                                   label=ugettext_lazy('UPDATE-PASSWORD-OLDPSW'))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False),
                                   label=ugettext_lazy('UPDATE-PASSWORD-NEWPSW'))
    new_password_again = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False),
                                         label=ugettext_lazy('UPDATE-PASSWORD-CONFIRMPSW'))

    class Meta:
        model = User
        exclude = ('language', 'account', 'last_visit', 'roles', 'nick', 'grants', 'favourites', 'password')

    def action(self):
        return reverse('accounts.my_account')

    def clean_old_password(self):
        return hashlib.md5(self.cleaned_data.get('old_password')).hexdigest()

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            return hashlib.md5(new_password).hexdigest()
        return new_password

    def clean_new_password_again(self):
        new_password_again = self.cleaned_data.get('new_password_again')
        if new_password_again:
            return hashlib.md5(new_password_again).hexdigest()
        return new_password_again

    def clean(self):
        cleaned_data = super(MyAccountForm, self).clean()
        user = self.instance
        new_password = cleaned_data.get("new_password")

        email = cleaned_data.get("email")
        try:
            user2 = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user2.id != user.id:
                raise forms.ValidationError(ugettext_lazy('EMAIL-EXISTS'))

        if new_password:
            old_password = cleaned_data.get("old_password")
            if user.password != old_password:
                raise forms.ValidationError(ugettext_lazy('OLD-PASSWORD-MISMATCH'))

            new_password_again = cleaned_data.get("new_password_again")
            if new_password != new_password_again:
                raise forms.ValidationError(ugettext_lazy('NEW-PASSWORD-MISMATCH'))

        return cleaned_data
