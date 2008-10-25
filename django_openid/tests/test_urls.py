from django.conf.urls.defaults import *
from django_openid.registration import AuthRegistration
from django_openid.utils import create_urlconf

urlpatterns = create_urlconf('test_oid', AuthRegistration())
