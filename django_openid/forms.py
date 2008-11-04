from django import forms
import models
from django.conf import settings

class OpenIDInput(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.Select(choices=(
                        (u'yandex', u'Yandex'),
                        (u'livejournal', u'LiveJournal'),
                        (u'openid', u'OpenID'))),
                   forms.TextInput)
        super(OpenIDInput, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        value = super(OpenIDInput, self).value_from_datadict(data, files, name)
        try:
            service, user = value
            return {u'yandex': u'http://openid.yandex.ru/%s/',
                    u'livejournal': u'http://%s.livejournal.com',
                    }.get(service, u'%s') % user
        except ValueError:
            return None

    def decompress(self, value):
        if value:
            for service, search in (
                (u'yandex', re.compile(r'openid.yandex.ru/(?P[a-zA-Z0-9-]+)').search),
                (u'livejournal', re.compile(r'(?P[a-zA-Z0-9-]+).livejournal.com').search)):
                result = search(value)
                if result:
                    return [service, result.group('user')]
            return [u'openid', value]
        return [None, None]

class OpenIDLoginForm(forms.Form):
    openid_url = forms.URLField(widget=OpenIDInput)

