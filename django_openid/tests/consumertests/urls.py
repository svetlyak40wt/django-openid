from django.conf.urls.defaults import *

urlpatterns = patterns('',
        (r'^basic/', include('consumertests.basic.urls')),
        (r'^session/', include('consumertests.session.urls')),
        (r'^cookie/', include('consumertests.cookie.urls')),
        (r'^urlconf/', include('consumertests.urlconf.urls')),
        (r'^auto/', include('consumertests.autoregistration.urls')),
)
