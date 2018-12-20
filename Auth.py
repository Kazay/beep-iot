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
import sys
import os
import json
import time
import datetime
from pprint import pprint
from LCD_display import LCD_display
from Sonar import Sonar

ledAuthorized = Led(11)
ledDenied = Led(12)

lcd = LCD_display()
sonar = Sonar(16, 18, 220)

# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()

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
	
def destroy():
	GPIO.cleanup()
	
def reset():
	ledAuthorized.off()
	ledDenied.off()
	lcd.lcd_clear()
	lcd.display_date()
	
if __name__ == "__main__":
	try:
		while(True):
			distance = sonar.getSonar()
			print ("The distance is : %.2f cm"%(distance))
			time.sleep(1)
			if distance < 30:
				while(True):
					reset()
					uid = scan()
					user = retrieve_json()
					if user['idRFID'] == uid:
						ledAuthorized.on()
						lcd.display_authorized(user)
					else:
						ledDenied.on()
						lcd.display_denied()
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()
 
	
