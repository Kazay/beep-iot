#!/usr/bin/env python3
########################################################################
# Filename    : Beep_bulk.py
# Description : Script handling RFID cards attribution
# author      : Kevin Czaja
# modification: 2019/01/12
########################################################################
import tkinter as tk
import tkinter.messagebox
import time
import MFRC522
import RPi.GPIO as GPIO
from Handle_GPIO import Handle_GPIO
from API_Requests import API_Requests
from functools import partial
from pprint import pprint

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root)
frame_main.grid(sticky='news')

frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas)
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# GPIO handler for RFID transistor
transistor_RFID = Handle_GPIO(11)
transistor_RFID.on()
# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()
api = API_Requests()

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
    uid = scan()
    r = api.update_rfid(userid, uid)
    pprint(r)
    if(r['code'] == 500):
        tk.messagebox.showinfo("Error", "Request failed, please check your connection and retry.")
    elif(r['code'] == 200):
        if(r['dupe'] == False):
            label_rfid[i].configure(text=uid)
        else:
            tk.messagebox.showinfo("Error", "Card is already assigned to another user.")

def deleteCallBack(userid, i):
    transistor_RFID = Handle_GPIO(11)
    transistor_RFID.on()
    mfrc = MFRC522.MFRC522()
    r = api.update_rfid(userid, '')
    pprint(r)
    label_rfid[i].configure(text='No RFID card')


label_lastname = []
label_firstname = []
label_rfid = []
button_assign = []
button_delete = []
users = api.get_all_users()

rows = len(users['list_of_users'])
for i in range(0, rows):
    pprint(users['list_of_users'][i]['rfid'])
    if(users['list_of_users'][i]['rfid'] == ['']):
        rfid = 'No RFID card'
    else:
        rfid = users['list_of_users'][i]['rfid']
    label_lastname.append(tk.Label(frame_buttons, text=users['list_of_users'][i]['lastname']))
    label_lastname[i].grid(row=i, column=0)
    label_firstname.append(tk.Label(frame_buttons, text=users['list_of_users'][i]['firstname']))
    label_firstname[i].grid(row=i, column=1)
    label_rfid.append(tk.Label(frame_buttons, text=rfid))
    label_rfid[i].grid(row=i, column=2)
    button_assign.append(tk.Button(frame_buttons, text ="Assign RFID", command = partial(assignCallBack,users['list_of_users'][i]['_id'],i)).grid(row=i, column=3))
    button_delete.append(tk.Button(frame_buttons, text ="Delete RFID", command = partial(deleteCallBack,users['list_of_users'][i]['_id'],i)).grid(row=i, column=4))

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = 470
first5rows_height = 600
frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                    height=first5rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

# Launch the GUI
root.mainloop()
