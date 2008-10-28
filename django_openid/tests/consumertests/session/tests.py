from django.test import TestCase
from django.core.urlresolvers import reverse

from openid_mocks import *
from mock_session import SessionStore

from openid.consumer import consumer as janrain_consumer

class SessionConsumerTest(TestCase):
    
    def login(self):
        openid_consumer = MySessionConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('osession-complete'), {'openid-args': 'go-here'})
        self.assertEqual(302, response.status_code)
        return response.request, response
    
    def testLogin(self):
        "Simulate a successful login"
        request, response = self.login()
        session = SessionStore()
        self.assertEqual(response['Location'], 'http://testserver/')
        self.assert_('openids' in session)
        self.assertEqual(len(session['openids']), 1)
        self.assertEqual(
            session['openids'][0].openid, 'http://simonwillison.net/'
        )
    
    def testLogout(self):
        request, response = self.login()
        response = self.client.get(reverse('osession-logout'))
        self.assertRedirects(response, '/')
        session = SessionStore()
        self.assertEqual(len(session['openids']), 0)

