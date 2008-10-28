from django.test import TestCase
from django.core.urlresolvers import resolve, Resolver404, reverse, NoReverseMatch

class URLConfTest(TestCase):
    def testCreateURLConf(self):
        self.assert_(resolve('/consumer/urlconf/openid/'))
        self.assert_(resolve('/consumer/urlconf/openid/complete/'))

        self.assertRaises(Resolver404, resolve, '/consumer/urlconf/openid/blah/')

    def testReverseByName(self):
        self.assert_(reverse('urlconf-index'))
        self.assert_(reverse('urlconf-complete'))
        self.assertRaises(NoReverseMatch, reverse, 'urlconf-blah')

