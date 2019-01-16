#!/usr/bin/env python3
########################################################################
# Filename    : Auth.py
# Description : Script handling raspberry
# author      : Kevin Czaja
# modification: 2019/01/09
########################################################################
import RPi.GPIO as GPIO
from Handle_GPIO import Handle_GPIO
from API_Requests import API_Requests
import MFRC522
import sys
import os
import json
import time
import datetime
from pprint import pprint
from LCD_display import LCD_display
from Sonar import Sonar

def components_idle():
	transistor_LCD.off()
	transistor_LCD_ground.off()
	transistor_RFID.off()
	
def components_active():
	transistor_LCD.on()
	transistor_LCD_ground.on()
	transistor_RFID.on()

def scan():
	timeout = time.time() + 20
	pprint('Scan your card')
	while (True):
		lcd.display_date(1)
		time.sleep(.5)
		# Scan for cards  
		(status,TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
		# If a card is found
		if status == mfrc.MI_OK:
			print ("Card detected")
			# Get the UID of the card
			(status,uid) = mfrc.MFRC522_Anticoll()		
			# If we have the UID, continue
			if status == mfrc.MI_OK:
				# Select the scanned tag
				if mfrc.MFRC522_SelectTag(uid) == 0:
					print ("MFRC522_SelectTag Failed!")
				return uid
		if time.time() > timeout:
			pprint('Timeout')
			break
	
def destroy():
	GPIO.cleanup()
	
def reset():
	ledAuthorized.off()
	ledDenied.off()
	lcd.lcd_clear()
	lcd.display_date(1)

if __name__ == "__main__":
	try:
		# GPIO handler for RFID transistor
		transistor_RFID = Handle_GPIO(11)
		# GPIO handler for 1st LCD display transistor
		transistor_LCD = Handle_GPIO(12)
		# GPIO handler for 2nd LCD display transistor
		transistor_LCD_ground = Handle_GPIO(40)
		# GPIO handler for green LED
		ledAuthorized = Handle_GPIO(13)
		# GPIO handler for red led
		ledDenied = Handle_GPIO(15)
		components_active()
		# GPIO handler for ultrasonic range device
		sonar = Sonar(16, 18, 300)
		# Create an object of the class MFRC522
		mfrc = MFRC522.MFRC522()
		
		api = API_Requests()
		lcd = LCD_display()
		components_idle()
		while(True):
			time.sleep(2)
			distance = sonar.getSonar()
			print ("The distance is : %.2f cm"%(distance))
			if distance < 50:
				components_active()
				while(True):
					reset()
					distance = sonar.getSonar()
					if distance > 50 :
						components_idle()
						break
					uid = scan()
					if(uid != None):
						data = api.user_authentication(uid)
						if 'authorized' in data and data['authorized'] == True:
							ledAuthorized.on()
							lcd.display_authorized(data)
						else:
							ledDenied.on()
							lcd.display_denied()
						del data
					time.sleep(2)
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()
