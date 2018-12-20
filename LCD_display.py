# requires RPi_I2C_driver.py
from LCD_driver import lcd
from time import *
import datetime

class LCD_display(lcd):

        def display_name(self, user):
                lcd.lcd_clear(self)
                line1 = 'Hi, ' + user['firstName'] + ' ' + user['lastName']
                line2 = 'Enjoy your class'
                self.display_scrolling(line1, 1)
                self.display_scrolling(line2, 2)
                sleep(2) # 2 sec delay
                lcd.lcd_clear(self)

        def display_idle(self):
                currentDate = datetime.datetime.now()
                lcd.lcd_display_string(self, currentDate.strftime('%d-%m-%Y'), 1)
                lcd.lcd_display_string(self, currentDate.strftime('%H:%M:%S'), 2)
                
        def display_denied(self):
                lcd.lcd_clear(self)
                lcd.lcd_display_string(self, 'Access denied,', 1)
                lcd.lcd_display_string(self, 'sorry pal.', 2)
                sleep(1) # 1 sec delay
                lcd.lcd_clear(self)
                
        def display_scrolling(self, string, line):
                i = 0
                if len(string) > 16:
                        while i < (len(string) - 15):
                                lcd.lcd_display_string(self, string[i:] , line)
                                sleep(1)
                                i += 1
                else:
                        lcd.lcd_display_string(self, string, line)    
