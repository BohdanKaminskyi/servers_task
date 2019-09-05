import json
from src.requests.request import Request


class RequestJSONSerializer:
    """Serializes/deserializes Request"""
    @staticmethod
    def serialize(request: Request) -> str:
        """Serializes request to json-string"""
        obj = {
            'headers': request.headers,
            'data': request.data
        }

        return json.dumps(obj)

    @staticmethod
    def deserialize(json_string: str) -> Request:
        """ Deserializes json-string to request"""
        return Request(**json.loads(json_string))
