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
