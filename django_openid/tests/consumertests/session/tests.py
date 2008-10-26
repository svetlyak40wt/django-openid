from django.test import TestCase
from django.http import Http404
from django_openid.consumer import Consumer
from django_openid import signed
from django.core.urlresolvers import reverse

from request_factory import RequestFactory
from openid_mocks import *
from mock_session import SessionStore

from openid.consumer import consumer as janrain_consumer

from pdb import set_trace

rf = RequestFactory()

class SessionConsumerTest(TestCase):
    
    def login(self):
        openid_consumer = MySessionConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('osession-complete'), {'openid-args': 'go-here'})
        self.assertEqual(302, response.status_code)
        #get.session = MockSession()
        #response = openid_consumer(get, 'complete/')
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
        #get.session = request.session
        #openid_consumer = MySessionConsumer()
        #response = openid_consumer(get, 'logout/')
        self.assertRedirects(response, '/')
        #self.assertEqual(response['Location'], '/')
        session = SessionStore()
        self.assertEqual(len(session['openids']), 0)

