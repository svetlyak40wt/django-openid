from django.conf.urls.defaults import *

urlpatterns = patterns('',
        (r'^session/', include('consumertests.session.urls')),
)
