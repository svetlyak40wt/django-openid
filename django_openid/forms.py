import re

from django import forms
import models
from django.conf import settings
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

