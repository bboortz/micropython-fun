
import sys
import traceback

from core.logger import Logger



#
# class
#
class GenericException(Exception):
    def __init__(self, context, message, cause):
        self.context = context
        self.message = message
        self.cause = cause


    def __str__(self):
        # return "{}: {}\n  context: {}\n  cause: {}".format(self.__fullname, self.message, self.context, self.cause)
        return "{}\n  context: {}\n  cause: {}".format(self.message, self.context, self.cause)


    def print(self):
        #print(self)
        print(traceback.format_exc())



class GenericClass:

    def __init__(self, task_name):
        self.task_name = task_name
        self.__fullname = self.fullname(self)
        self.LOG = Logger(self.__fullname, self.task_name)


    def fullname(self, o):
        klass = o.__class__
        module = klass.__module__
        if module == 'builtins':
            return klass.__qualname__ # avoid outputs like 'builtins.str'
        return module + '.' + klass.__qualname__
