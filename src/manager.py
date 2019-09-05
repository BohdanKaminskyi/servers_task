from src.helpers import Singleton


class MessageManager(metaclass=Singleton):
    """Manage:
        - serializing/deserializing of messages
        - checking if message conforms to defined protocol
        - execute commands
    """
    def __init__(self,
                 serializer,
                 executor,
                 protocol):
        self.serializer = serializer
        self.executor = executor
        self.protocol = protocol

    def get_request(self, message):
        return self.serializer.deserialize(message)

    def validate_header(self, message):
        request = self.get_request(message)
        headers = request.headers

        if not headers.get('Auth'):
            return False
        return True
