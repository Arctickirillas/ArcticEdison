# -*- coding: utf8 -*-
import pyupm_i2clcd
import time

class LCDScreen:
    def __init__(self, state = 0):
        self.lcd = pyupm_i2clcd.Jhd1313m1(0, 0x3E, 0x62)
        self.lcd.clear()
        self.lcd.setColor(255,255,255)
        self.lcd.setCursor(0, 0)
        self.lcd.write('Loading...')
    


    # States:
    def setLCDState(self, state):
        # quiet/blue = 0
        if state == 0:
            self.lcd.setColor(100,149,237)
        # normal/green = 1
        elif state == 1:
            self.lcd.setColor(0,255,0)
        # noisily/yellow = 2
        elif state == 2:
            self.lcd.setColor(255,255,0)
        # veryLoud/red = 3
        elif state == 3:
            self.lcd.setColor(255,0,0)



    def setOption(self, title, status):
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        self.lcd.write(str(title)+':')
#        self.lcd.setCursor(1,0)
        self.lcd.write(str(status))

#lcd = LCDScreen(3)
#lcd.setOption('smth','hello')
#time.sleep(200)