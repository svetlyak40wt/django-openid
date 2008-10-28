from django.conf.urls.defaults import *

urlpatterns = patterns('',
        (r'^basic/', include('consumertests.basic.urls')),
        (r'^session/', include('consumertests.session.urls')),
)
