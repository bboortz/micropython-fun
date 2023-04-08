from neopixel import NeoPixel
 

class NeoLed:

    def __init__(self, pin, pixel_count):
           self.np = NeoPixel(pin, pixel_count)   # create NeoPixel driver on pin for n pixels

    def color(self, color_hex):
        self.np[0] = color_hex
        self.np.write()
