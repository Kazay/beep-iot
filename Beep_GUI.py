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
display.title('Beep bulk edit')
	
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
	
def assignCallBack(userid, i):
	transistor_RFID = Handle_GPIO(11)
	transistor_RFID.on()
	mfrc = MFRC522.MFRC522()
	tkinter.messagebox.showinfo("Assign RFID", "Assign RFID Card")
	uid = scan()
	api.update_rfid(userid, uid)
	label_rfid[i].configure(text=uid)

def deleteCallBack(userid, i):
	transistor_RFID = Handle_GPIO(11)
	transistor_RFID.on()
	mfrc = MFRC522.MFRC522()
	tkinter.messagebox.showinfo("Delete RFID", "Delete RFID Card assigned")
	api.update_rfid(userid, '')
	label_rfid[i].configure(text='')

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		label_lastname = []
		label_firstname = []
		label_rfid = []
		button_assign = []
		button_delete = []
		users = api.get_all_users()
		height = len(users['list_of_users'])
		for i in range(height): #Rows
			label_lastname.append(tkinter.Label(display, text=users['list_of_users'][i]['lastname']))
			label_lastname[i].grid(row=i, column=0)
			label_firstname.append(tkinter.Label(display, text=users['list_of_users'][i]['firstname']))
			label_firstname[i].grid(row=i, column=1)
			label_rfid.append(tkinter.Label(display, text=users['list_of_users'][i]['rfid']))
			label_rfid[i].grid(row=i, column=2)
			button_assign.append(tkinter.Button(display, text ="Assign RFID", command = partial(assignCallBack,users['list_of_users'][i]['_id'],i)).grid(row=i, column=3))
			button_delete.append(tkinter.Button(display, text ="Delete RFID", command = partial(deleteCallBack,users['list_of_users'][i]['_id'],i)).grid(row=i, column=4))
		display.mainloop()
		
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()
