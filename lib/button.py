from machine import Pin



# 
# global constants
#



#
# functions
#
def callback_button(p):
    print('*** button change', p)



#
# class
#
class ButtonException(BaseException):
    pass


class Button:

    def __init__(self, pin_no):
        self.pin_no = pin_no
        self.pin = Pin(pin_no, Pin.IN)

    def irq(self, trigger=Pin.IRQ_FALLING, callback=callback_button):
        self.pin.irq(trigger=trigger, handler=callback)

    def value(self):
        return self.pin.value()
