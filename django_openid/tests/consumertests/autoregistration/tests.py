from django.test import TestCase
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY as AUTH_SESSION_KEY

from openid_mocks import *
from mock_session import SessionStore, clear_session

from openid.consumer import consumer as janrain_consumer


class AutoRegisterTest(TestCase):
    def setUp(self):
        clear_session()
        super(AutoRegisterTest, self).setUp()

    def testCreateNewAccountOnLogin(self):
        "Simulate a successful registration"
        openid_consumer = MyAutoRegistration()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )

        response = self.client.get(reverse('oauto-complete'), {'openid-args': 'go-here'})

        self.assertRedirects(response, 'http://testserver/')

        session = SessionStore()
        self.assert_('openids' in session)

        #self.assert_(AUTH_SESSION_KEY not in session)
        #self.assertEqual(0, User.objects.count())

        #response = self.client.get(reverse('oauto-register'))
        #self.assertEqual(200, response.status_code)

        self.assert_(AUTH_SESSION_KEY in session)
        self.assertEqual(1, User.objects.count())

    def testDontCreateTwice(self):
        "Simulate a successful registration"
        openid_consumer = MyAutoRegistration()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )

        def register():
            clear_session()
            response = self.client.get(reverse('oauto-complete'), {'openid-args': 'go-here'})
            response = self.client.get(reverse('oauto-register'))
            self.assertEqual(200, response.status_code)

        register()
        register()

        session = SessionStore()
        self.assert_(AUTH_SESSION_KEY in session)
        self.assertEqual(1, User.objects.count())

