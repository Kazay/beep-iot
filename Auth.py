#!/usr/bin/env python3
########################################################################
# Filename    : Auth.py
# Description : Script handling raspberry
# author      : Kevin Czaja
# modification: 2019/01/09
########################################################################
import RPi.GPIO as GPIO
from Handle_GPIO import Handle_GPIO
import MFRC522
import sys
import os
import json
import time
import datetime
from pprint import pprint
from LCD_display import LCD_display
from Sonar import Sonar

# GPIO handler for RFID transistor
transistor_RFID = handle_GPIO(11)
# GPIO handler for 1st LCD display transistor
transistor_LCD = handle_GPIO(12)
# GPIO handler for 2nd LCD display transistor
transistor_LCD_ground = handle_GPIO(40)
# GPIO handler for green LED
ledAuthorized = handle_GPIO(13)
# GPIO handler for red led
ledDenied = handle_GPIO(15)
# GPIO handler for ultrasonic range device
sonar = Sonar(16, 18, 300)
# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()

# Trigger Ultrasonic Range
# If distance < 30
	# Turn transistors pin ON
	# Clean display & display current datetime (default display)
	# Until a card is detected
		# If distance >= 30
			# Turn transistors pin OFF
			# Break
		# Scan RFID card (timeout 60s)
		# Call API to check credentials
		# if card UID is recognized
			# Turn ON green led
			# Display user information on LCD screen
		# else
			# Turn ON red led
			# Display error

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
					user = retrieve_json(uid)
					if user['idRFID'] == uid:
						ledAuthorized.on()
						#send_records(user[_id])
						lcd.display_authorized(user)

					else:
						ledDenied.on()
						lcd.display_denied()
					time.sleep(1)
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()
 

def components_idle():
	transistor_LCD.off()
	transistor_LCD_ground.off()
	transistor_RFID.off()
	
def components_active():
	transistor_LCD.on()
	transistor_LCDBIS_ground.on()
	transistor_RFID.on()

def retrieve_json(uid):
	userInfos = ""
	# TO DO: API call to retrieve
	response = requests.get("http://ebcitakademy.alwaysdata.net/users/uid/%"%uid)
	if(response.status_code == 200):
		userInfos = response.data
		#userInfos = json.loads(jsonTest)
	return userInfos

def send_records(idUser):
	# Store current datetime
	# build JSON
	# API post request
	# return response

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
	
