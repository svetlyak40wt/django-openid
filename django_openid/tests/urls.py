from django.conf.urls.defaults import *

urlpatterns = patterns('',
        (r'^/$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
        (r'^content/$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
        (r'^consumer/', include('consumertests.urls')),
)
