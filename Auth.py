#!/usr/bin/env python3
########################################################################
# Filename    : RFID.py
# Description : Use MFRC522 read and write Mifare Card.
# auther      : www.freenove.com
# modification: 2018/09/08
########################################################################
import RPi.GPIO as GPIO
import MFRC522
from Led import Led
from Transistor import Transistor
import sys
import os
import json
import time
import datetime
from pprint import pprint
from LCD_display import LCD_display
from Sonar import Sonar

transistorRFID = Transistor(11)
transistorLCD = Transistor(12)
transistorLCDBIS = Transistor(40)
ledAuthorized = Led(13)
ledDenied = Led(15)
sonar = Sonar(16, 18, 300)

# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()

def components_idle():
	transistorLCD.off()
	transistorLCDBIS.off()
	transistorRFID.off()
	
def components_active():
	transistorLCD.on()
	transistorLCDBIS.on()
	transistorRFID.on()

def retrieve_json():
	# TO DO: API call to retrieve
	userInfos = {
				'_id': 1, 'firstName' : 'Uvuvuwewe',
				'lastName' : 'Czaja',
				'mail' : 'czajakevin@gmail.com',
				'dateOfBirth' : '09-26-1988',
				'idRFID': [1, 82, 76, 115, 108]
				}
				
	#userInfos = json.loads(jsonTest)
	
	return userInfos

def scan():
	timeout = time.time() + 60
	while (True):
		lcd.display_date()
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
			break
		if time.time() > timeout:
			break
	
def destroy():
	GPIO.cleanup()
	
def reset():
	ledAuthorized.off()
	ledDenied.off()
	lcd.lcd_clear()
	lcd.display_date()
	
if __name__ == "__main__":
	try:
		components_active()
		#components_idle()
		while(True):
			time.sleep(2)
			distance = sonar.getSonar()
			print ("The distance is : %.2f cm"%(distance))
			if distance < 30:
				#components_active()
				lcd = LCD_display()
				while(True):
					reset()
					distance = sonar.getSonar()
					if distance > 30:
						 #components_idle()
						break
					uid = scan()
					user = retrieve_json()
					if user['idRFID'] == uid:
						ledAuthorized.on()
						lcd.display_authorized(user)
					else:
						ledDenied.on()
						lcd.display_denied()
					time.sleep(1)
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()
 
	
