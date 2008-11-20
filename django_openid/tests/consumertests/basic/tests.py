from django.test import TestCase
from django.core.urlresolvers import reverse, NoReverseMatch

from openid_mocks import *
from mock_session import SessionStore

from openid.consumer import consumer as janrain_consumer

class ConsumerTest(TestCase):
    
    def testBadMethod(self):
        "Non existent methods should result not be in the URLConf"
        self.assert_(reverse('obasic-index'))
        self.assertRaises(NoReverseMatch, reverse, 'obasic-foo')
    
    def testLoginBegin(self):
        "Can log in with an OpenID"
        session = SessionStore()
        self.assert_('openid_bits' not in session)

        response = self.client.post(reverse('obasic-index'), {
            'openid_url_0': 'openid',
            'openid_url_1': 'http://simonwillison.net/'
        })

        self.assertRedirects(response, 'http://url-of-openid-server/')
        session = SessionStore()
        self.assert_('openid_bits' in session)
    
    def testLoginDiscoverFail(self):
        "E.g. the user enters an invalid URL"
        openid_consumer = MyConsumer()
        openid_consumer.raise_discover_failure = True
        response = self.client.post(reverse('obasic-index'), {
            'openid_url_0': 'openid',
            'openid_url_1': 'http://not-an-openid.com'
        })
        self.assertContains(response, openid_consumer.openid_invalid_message)
    
    def testLoginSuccess(self):
        "Simulate a successful login"
        openid_consumer = MyConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('obasic-complete'), {'openid-args': 'go-here'})
        self.assertContains(response, 'You logged in as http://simonwillison.net/')
    
    def testLoginNext(self):
        "?next=<signed> causes final redirect to go there instead"
        openid_consumer = MyConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SUCCESS,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('obasic-complete'), {
            'openid-args': 'go-here',
            'next': openid_consumer.sign_done('/content/')
        })
        self.assertRedirects(response, '/content/')
    
    def testLoginCancel(self):
        openid_consumer = MyConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.CANCEL,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('obasic-complete'), {'openid-args': 'go-here'})
        self.assert_(
            openid_consumer.request_cancelled_message in response.content
        )
    
    def testLoginFailure(self):
        openid_consumer = MyConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.FAILURE,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('obasic-complete'), {'openid-args': 'go-here'})
        self.assertContains(response, 'Failure:')
    
    def testLoginSetupNeeded(self):
        openid_consumer = MyConsumer()
        openid_consumer.set_mock_response(
            status = janrain_consumer.SETUP_NEEDED,
            identity_url = 'http://simonwillison.net/',
        )
        response = self.client.get(reverse('obasic-complete'), {'openid-args': 'go-here'})
        self.assertContains(response, openid_consumer.setup_needed_message)
    
    def testLogo(self):
        openid_consumer = MyConsumer()
        response = self.client.get(reverse('obasic-logo'))
        self.assert_('image/gif' in response['Content-Type'])

