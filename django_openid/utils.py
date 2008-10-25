from openid.yadis import xri
import datetime

class OpenID:
    def __init__(self, openid, issued, sreg=None):
        self.openid = openid
        self.issued = issued # datetime (used to be int(time.time()))
        self.sreg = sreg or {}
    
    def is_iname(self):
        return xri.identifierScheme(self.openid) == 'XRI'
    
    def __repr__(self):
        return '<OpenID: %s>' % self.openid
    
    def __unicode__(self):
        return self.openid
    
    @classmethod
    def from_openid_response(cls, openid_response):
        return cls(
            openid = openid_response.identity_url,
            issued = datetime.datetime.now(),
            sreg = openid_response.extensionResponse('sreg', False)
        )

def create_urlconf(prefix, obj):
    from django.conf.urls.defaults import patterns
    if prefix and prefix[-1] != '/':
        prefix += '/'

    ptns = patterns('',)
    for key in dir(obj):
        if key.startswith('do_'):
            view = key[3:]
            view_name = 'openid-' + view
            view = (view != 'index') and (view + '/') or ''

            view_pattern = r'^%s%s$' % (prefix, view)
            ptns += patterns('', (view_pattern, getattr(obj, key), {}, view_name))
    return ptns
