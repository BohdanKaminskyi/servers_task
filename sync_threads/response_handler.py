import json


class Response:
    """
    Response is used to create and encode/decode messages.
    """

    def __init__(self, content='', status=200):
        self.content = content
        self.status = status

    def _to_dict(self):
        """
        Pack content and status into dict.
        """
        return {
            'content': self.content,
            'status': self.status
        }

    def encode(self, encoding):
        """
        Encode the response using the codec registered for encoding.
        """
        return json.dumps(self._to_dict()).encode(encoding=encoding)

    @staticmethod
    def decode(response):
        """
        Decode the response from json string.
        """
        return Response(**json.loads(response))

    def __repr__(self):
        return f'Response(status={self.status}, content={repr(self.content)})'
