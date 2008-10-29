from django.contrib.sessions.backends.cache import SessionStore as CachedSession

_mock_session = CachedSession()

def SessionStore(session_key = None):
    return _mock_session

def clear_session():
    global _mock_session
    _mock_session = CachedSession()

