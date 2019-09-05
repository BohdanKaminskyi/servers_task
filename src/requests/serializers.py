import json
from src.requests.request import Request
from src.requests.response import Response


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


class ResponseJSONSerializer:
    """Serializes/deserializes Response"""
    @staticmethod
    def serialize(response: Response) -> str:
        """Serializes response to json-string"""
        obj = {
            'status': response.status,
            'data': response.data
        }

        return json.dumps(obj)

    @staticmethod
    def deserialize(json_string: str) -> Response:
        """ Deserializes json-string to response"""
        return Response(**json.loads(json_string))
