from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from openid.server.server import Server
from openid.extensions import sreg

from django_openid.models import DjangoOpenIDStore
from django_openid.utils import encode_object, decode_object

class OpenIDServer(object):
    """
    The default OpenID server, designed to be subclassed.
    """
    this_is_a_server_template = 'django_openid/this_is_an_openid_server.html'
    landing_page_template = 'django_openid/landing_page.html'
    error_template = 'django_openid/error.html'
    decide_template = 'django_openid/decide.html'
    
    not_your_openid_message = 'You are signed in but do not own that OpenID'
    invalid_decide_post_message = 'Your submission cannot be processed'
    
    save_trusted_roots = False # If true, tries to persist trusted roots
    secret_key = None
    
    def get_server(self, request):
        return Server(DjangoOpenIDStore())
    
    def user_is_logged_in(self, request):
        return False
    
    def openid_is_authorized(self, request, openid, trust_root):
        return self.user_is_logged_in(request) and \
            self.user_owns_openid(request, openid) and \
            self.user_trusts_root(request, openid, trust_root)
    
    def user_owns_openid(self, request, openid):
        return False
    
    def user_trusts_root(self, request, openid, trust_root):
        # Over-ride to implement trust root whitelisting style functionality
        return False
    
    def server_response(self, request, oresponse):
        webresponse = self.get_server(request).encodeResponse(oresponse)
        response = HttpResponse(webresponse.body)
        response.status_code = webresponse.code
        for key, value in webresponse.headers.items():
            response[key] = value
        return response
    
    def show_landing_page(self, request, orequest):
        return render_to_response(self.landing_page_template, {
            'identity_url': orequest.identity,
        })
    
    def show_error(self, request, message):
        return render_to_response(self.error_template, {
            'message': message,
        })
    
    def show_decide(self, request, orequest):
        # If user is logged in, ask if they want to trust this trust_root
        # If they are NOT logged in, show the landing page:
        if not self.user_is_logged_in(request):
            return self.show_landing_page(request, orequest)
        
        # Check that the user owns the requested identity
        if not self.user_owns_openid(request, orequest.identity):
            return self.show_error(request, self.not_your_openid_message)
        
        # They are logged in - ask if they want to trust this root
        return render_to_response(self.decide_template, {
            'trust_root': orequest.trust_root,
            'identity': orequest.identity,
            'orequest': encode_object(orequest, self.secret_key),
            'action': request.path,
            'save_trusted_roots': self.save_trusted_roots
        })
    
    def get_sreg_data(self, request, openid):
        return {}
    
    def add_sreg_data(self, request, orequest, oresponse):
        sreg_req = sreg.SRegRequest.fromOpenIDRequest(orequest)
        sreg_resp = sreg.SRegResponse.extractResponse(
            sreg_req, self.get_sreg_data(request, orequest.identity)
        )
        oresponse.addExtension(sreg_resp)
    
    def save_trusted_root(self, request, openid, trust_root):
        pass
    
    def process_decide(self, request):
        try:
            orequest = decode_object(
                request.POST.get('orequest', ''), self.secret_key
            )
        except ValueError:
            return self.show_error(self.invalid_decide_post_message)
        
        they_said_yes = bool(
            ('yes_once' in request.POST) or
            ('yes_always' in request.POST)
        )
        if 'yes_always' in request.POST:
            self.save_trusted_root(
                request, orequest.identity, orequest.trust_root
            )
        
        # TODO: Double check what we should be passing as identity= here:
        oresponse = orequest.answer(they_said_yes, identity=orequest.identity)
        self.add_sreg_data(request, orequest, oresponse)
        return self.server_response(request, oresponse)
    
    def __call__(self, request):
        # If this is a POST from the decide page, behave differently
        if '_decide' in request.POST:
            return self.process_decide(request)
        
        querydict = dict(request.REQUEST.items())
        orequest = self.get_server(request).decodeRequest(querydict)
        if not orequest:
            return self.show_this_is_an_openid_server(request)
        
        if orequest.mode in ("checkid_immediate", "checkid_setup"):
            if self.openid_is_authorized(
                    request, orequest.identity, orequest.trust_root
                ):
                oresponse = orequest.answer(True)
            elif orequest.immediate:
                oresponse = orequest.answer(
                    False, request.build_absolute_uri()
                )
            else:
                return self.show_decide(request, orequest)
        else:
            oresponse = self.get_server(request).handleRequest(orequest)
        return self.server_response(request, oresponse)
    
    def show_this_is_an_openid_server(self, request):
        return render_to_response(self.this_is_a_server_template)
