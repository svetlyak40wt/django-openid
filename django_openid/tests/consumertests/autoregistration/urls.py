from django.conf.urls.defaults import *
from django_openid.utils import create_urlconf

from openid_mocks import *

urlpatterns = create_urlconf('openid', MyAutoRegistration())
