class MockSession(dict):
    def __init__(self, **kwargs):
        super(MockSession, self).__init__(**kwargs)
        self.modified = False


_mock_session = MockSession()

def SessionStore(session_key = None):
    return _mock_session
