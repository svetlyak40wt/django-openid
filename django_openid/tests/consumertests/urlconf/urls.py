from django.conf.urls.defaults import *
from django_openid.utils import create_urlconf

from openid_mocks import *

class Test(object):
    def do_index(self):
        return True

    def do_complete(self):
        return True

urlpatterns = create_urlconf('openid', Test(), 'urlconf')
