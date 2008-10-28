from django.test import TestCase
from django_openid import signed
from django.core.urlresolvers import reverse

from openid_mocks import *

from openid.consumer import consumer as janrain_consumer

class CookieConsumerTest(TestCase):
    
    def login(self):
        openid_consumer = MyCookieConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('ocookie-complete'), {'openid-args': 'go-here'})
        return response
    
    def testLogin(self):
        "Simulate a successful login"
        response = self.login()
        self.assert_('openid' in response.cookies, 'openid cookie not set')
        self.assertRedirects(response, '/')
        # Decrypt the cookie and check it's the right thing
        cookie = response.cookies['openid'].value
        openid = signed.loads(cookie)
        self.assertEqual(openid.openid, 'http://simonwillison.net/')
    
    def testLogout(self):
        self.login()
        response = self.client.get(reverse('ocookie-logout'))
        self.assert_('openid' in response.cookies, 'openid cookie not set')
        self.assertRedirects(response, '/')
        self.assertEqual(response.cookies['openid'].value, '')

