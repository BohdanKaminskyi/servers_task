class Request:
    """Handle request from user"""
    def __init__(self, *_, data: dict, headers: dict):
        self.data = data
        self.headers = headers

    def __repr__(self):
        return f'Request(headers={self.headers}, data={self.data}'
