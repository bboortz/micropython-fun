
#
# class
#

class Logger():
    
    def __init__(self, component, task = "core"):
        self.__component = component
        self.__task = task


    def print_generic(self, lvl, task, component, msg):
        print('-{0: <3} {1: <15} [{2: <30}] {3}'.format(lvl, task, component, msg))


    def print_cmd(self, msg):
        s = "{} ...".format(msg)
        self.print_generic(">", self.__task, self.__component, s)


    def print_info(self, msg):
        self.print_generic("I", self.__task, self.__component, msg)


    def print_error(self, msg):
        self.print_generic("E", self.__task, self.__component, msg)


    def print_wait(self):
        print('.', end='')

