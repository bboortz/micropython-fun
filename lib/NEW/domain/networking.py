import abc

from core.generic import GenericClass, GenericException



#
# class
#
class NetworkingException(GenericException):
    def __init__(self, message, cause):
        context = "domain"
        super().__init__(context, message, cause)



class Networking(GenericClass, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError


    @abc.abstractmethod
    def disconnect(self, force=False):
        raise NotImplementedError
