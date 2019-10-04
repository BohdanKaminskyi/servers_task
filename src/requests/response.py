class Response:
    """Handle response from server"""
    def __init__(self, *_, data='', status=200):
        self.data = data
        self.status = status

    def __repr__(self):
        return f'Response(status={self.status}, data={repr(self.data)})'
