


#
# class
#

class Logger():
    
    def __init__(self, component, task_name = "core", log_debug = False):
        self.__component = component
        self.__task_name = task_name
        self.log_debug = log_debug


    def print_generic(self, lvl, task_name, component, msg):
        print('-{0: <3} {1: <15} [{2: <30}] {3}'.format(lvl, task_name, component, msg))


    def print_cmd(self, msg):
        s = "{} ...".format(msg)
        self.print_generic(">", self.__task_name, self.__component, s)


    def print_info(self, msg):
        self.print_generic("I", self.__task_name, self.__component, msg)


    def print_debug(self, msg):
        if self.log_debug:
            self.print_generic("D", self.__task_name, self.__component, msg)


    def print_error(self, msg):
        self.print_generic("E", self.__task_name, self.__component, msg)


    def print_wait(self):
        print('.', end='')

