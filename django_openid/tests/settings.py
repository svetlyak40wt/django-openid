DATABASE_ENGINE='sqlite3'
SESSION_ENGINE='mock_session'
DEBUG_PROPAGATE_EXCEPTIONS=True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_openid.registration.AutoRegistration',
 )
