from django.conf import settings
from django.template import Library

from django_openid import signed

register = Library()

def sign(value):
    '''Use this filter to encode 'next' attribute and pass it to the openid views.'''
    return signed.dumps(value, extra_salt = settings.SECRET_KEY)

register.filter(sign)
