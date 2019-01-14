#!/usr/bin/env python3
import tkinter
import tkinter.messagebox
import time
import MFRC522
import RPi.GPIO as GPIO
from Handle_GPIO import Handle_GPIO
from pprint import pprint
from API_Requests import API_Requests
from functools import partial

# GPIO handler for RFID transistor
transistor_RFID = Handle_GPIO(11)
# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()
api = API_Requests()
display = tkinter.Tk()

def assignCallBack(userid):
	transistor_RFID = Handle_GPIO(11)
	transistor_RFID.on()
	mfrc = MFRC522.MFRC522()
	tkinter.messagebox.showinfo("Assign RFID", "Assign RFID Card")
	uid = scan()
	api.update_rfid(userid, uid)
	display_table()

def deleteCallBack(userid):
	transistor_RFID = Handle_GPIO(11)
	transistor_RFID.on()
	mfrc = MFRC522.MFRC522()
	tkinter.messagebox.showinfo("Delete RFID", "Delete RFID Card assigned")
	api.update_rfid(userid, '')
	
	display_table()
	
def scan():
	while (True):
		time.sleep(.5)
		# Scan for cards  
		(status,TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
		pprint('Scan for card')
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
			
def display_table():
	users = api.get_all_users()
	height = len(users)
	width = 4
	for i in range(height): #Rows
		for j in range(width): #Columns
			label_lastname = tkinter.Label(display, text=users['list_of_users'][i]['lastname']).grid(row=i, column=0)
			label_firstname = tkinter.Label(display, text=users['list_of_users'][i]['firstname']).grid(row=i, column=1)
			label_rfid = tkinter.Label(display, text=users['list_of_users'][i]['rfid']).grid(row=i, column=2)
			button_assign = tkinter.Button(display, text ="Assign RFID", command = partial(assignCallBack,users['list_of_users'][i]['_id'])).grid(row=i, column=3)
			button_delete = tkinter.Button(display, text ="Delete RFID", command = partial(deleteCallBack,users['list_of_users'][i]['_id'])).grid(row=i, column=4)
	display.mainloop()

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		display_table()
		
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()

