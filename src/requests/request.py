class Request:
    """Handle request from user"""
    def __init__(self, *_, data: dict, headers: dict):
        self.data = data
        self.headers = headers
