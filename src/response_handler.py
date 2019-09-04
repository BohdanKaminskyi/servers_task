import json


class Response:
    """Handle responses

    Create and encode/decode messages"""

    def __init__(self, user_id='', content='', status=200):
        self.user_id = user_id
        self.content = content
        self.status = status

    def _to_dict(self):
        """Pack content and status into dict

        :returns: dict containing content and status of response
        :rtype: dict
        """
        return {
            'user_id': self.user_id,
            'content': self.content,
            'status': self.status
        }

    def encode(self, encoding: str) -> str:
        """Encode the response using the codec registered for encoding

        :param encoding: Encoding to be used
        :type encoding: str
        :returns: json string with encoded data
        :rtype: str
        """
        return json.dumps(self._to_dict()).encode(encoding=encoding)

    @staticmethod
    def decode(response):
        """Decode the response from json string

        :param response: json string to decoded
        :type response: str
        :returns: Response object with response data
        :rtype: Response
        """
        return Response(**json.loads(response))

    def __repr__(self):
        return f'Response(status={self.status}, content={repr(self.content)}, user_id={self.user_id})'
