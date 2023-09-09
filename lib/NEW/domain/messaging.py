import abc

from core.generic import GenericClass, GenericException



#
# class
#
class MessagingException(GenericException):
    def __init__(self, message, cause):
        context = "domain"
        super().__init__(context, message, cause)



class Messaging(GenericClass, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError


    @abc.abstractmethod
    def disconnect(self, force=False):
        raise NotImplementedError


    @abc.abstractmethod
    def publish(self, topic, msg):
        raise NotImplementedError


    @abc.abstractmethod
    def subscribe(self, topic, message_func):
        raise NotImplementedError


    @abc.abstractmethod
    def send_alive(self):
        raise NotImplementedError


    @abc.abstractmethod
    def ping(self) -> bool:
        raise NotImplementedError


    @abc.abstractmethod
    def wait_msg(self):
        raise NotImplementedError
