import json


class ResponseHandler:
    """ResponseHandler is used to encode/decode messages."""

    @staticmethod
    def encode(obj: dict):
        if 200 <= obj['status'] <= 300:
            return json.dumps(
                {
                    'status': obj['status'],
                    'data': obj['data']
                }
            )
        else:
            return json.dumps(
                {
                    'status': obj['status'],
                    'error': {
                        'message': obj['message']
                    }
                }
            )

    @staticmethod
    def decode(response: str):
        return json.loads(response)
