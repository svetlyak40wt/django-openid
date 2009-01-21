import re

from django import forms
import models
from django.conf import settings
from django.contrib.auth.models import User
from django_openid.settings import DEFAULT_SERVICES

_services = getattr(settings, 'OPENID_SERVICES', DEFAULT_SERVICES)

_service_choices = sorted((service, name) for service, (name, _, _) in _services.iteritems())
_service_urls = dict((service, url) for service, (_, url, _) in _services.iteritems())
_service_patterns = list((service, re.compile(pattern or (url % '(?P<user>.*)')).search) for service, (_, url, pattern) in _services.iteritems())


class OpenIDInput(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.Select(choices=_service_choices),
                   forms.TextInput)
        super(OpenIDInput, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        value = super(OpenIDInput, self).value_from_datadict(data, files, name)
        try:
            service, user = value
            print  _service_urls.get(service, u'%s') % user
            return _service_urls.get(service, u'%s') % user
        except ValueError:
            return None

    def decompress(self, value):
        if value:
            for service, search in _service_patterns:
                result = search(value)
                if result:
                    return [service, result.group('user')]
            return [u'openid', value]
        return [None, None]

class OpenIDLoginForm(forms.Form):
    openid_url = forms.URLField(widget=OpenIDInput, initial='http://some.openid.com')

class RegistrationForm(forms.ModelForm):
    no_password_error = 'You must either set a password or attach an OpenID'
    invalid_username_error = 'Usernames must consist of letters and numbers'
    reserved_username_error = 'That username cannot be registered'
    
    username_re = re.compile('^[a-zA-Z0-9]+$')
    
    # Additional required fields (above what the User model says)
    extra_required = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        """
        Accepts openid as optional keyword argument, for password validation.
        Also accepts optional reserved_usernames keyword argument which is a
        list of usernames that should not be registered (e.g. 'security')
        """
        try:
            self.openid = kwargs.pop('openid')
        except KeyError:
            self.openid = None
        try:
            self.reserved_usernames = kwargs.pop('reserved_usernames')
        except KeyError:
            self.reserved_usernames = []
        
        # Super's __init__ creates self.fields for us
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Now we can modify self.fields with our extra required information
        for field in self.extra_required:
            self.fields[field].required = True
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    # Password is NOT required as a general rule; we only validate that they 
    # have set a password if an OpenID is not being associated
    password = forms.CharField(
        widget = forms.PasswordInput,
        required = False
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if not self.username_re.match(username):
            raise forms.ValidationError, self.invalid_username_error
        if username in self.reserved_usernames:
            raise forms.ValidationError, self.reserved_username_error
        return username
    
    def clean_password(self):
        "Password is only required if no OpenID was specified"
        password = self.cleaned_data.get('password', '')
        if not self.openid and not password:
            raise forms.ValidationError, self.no_password_error
        return password
    
    
    def save(self):
        user = User.objects.create(
            username = self.cleaned_data['username'],
            first_name = self.cleaned_data.get('first_name', ''),
            last_name = self.cleaned_data.get('last_name', ''),
            email = self.cleaned_data.get('email', ''),
        )
        # Set OpenID, if one has been associated
        if self.openid:
            user.openids.create(openid = self.openid)
        # Set password, if one has been specified
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            user.save()
        return user

class RegistrationFormPasswordConfirm(RegistrationForm):
    password_mismatch_error = 'Your passwords do not match'
    
    password2 = forms.CharField(
        widget = forms.PasswordInput,
        required = False,
        label = "Confirm password"
    )
    
    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password and (password != password2):
            raise forms.ValidationError, self.password_mismatch_error
        return password2
