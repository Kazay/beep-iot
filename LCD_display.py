# requires RPi_I2C_driver.py
from LCD_driver import lcd
from pprint import pprint
from time import *
import datetime
from collections import OrderedDict


class LCD_display(lcd):

        def display_authorized(self, user):
                lcd.lcd_clear(self)
                pprint(user)
                datas = ['Hi, ' + user['firstname'][0] + '. ' + user['lastname']]
                if(user['course'] != ''):
                        datas.insert(len(datas) + 1, user['course'])
                if(user['room'] != ''):
                        datas.insert(len(datas) + 1, 'Salle ' + user['room'])
                for data in datas:
                        self.display_date(1)
                        self.display_scrolling(data, 2)
                        sleep(2) # 2 sec delay
                        lcd.lcd_clear(self)
                
        def display_denied(self):
                lcd.lcd_clear(self)
                self.display_date(1)
                lcd.lcd_display_string(self, 'Access denied', 2)
                sleep(1) # 1 sec delay
                
        def display_date(self, pos):
                currentDate = datetime.datetime.now()
                lcd.lcd_display_string(self, currentDate.strftime('%d-%m-%y') + '   ' + currentDate.strftime('%H:%M'), pos)
                
        def display_scrolling(self, string, pos):
                i = 0
                if len(string) > 16:
                        while i < (len(string) - 15):         
                                lcd.lcd_display_string(self, string[i:] , pos)
                                sleep(0.5)
                                i += 1
                else:
                        lcd.lcd_display_string(self, string, pos)  
