#!/usr/bin/env python3

import requests
from pprint import pprint

class API_Requests:
		
	def get_user(self, uid):
		payload = {'id': uid}
		r = requests.get('http://ebcitakademy.alwaysdata.net/users/rfid?', params=payload)
		if(r.status_code == 200):
			data = r.json()
		else:
			data = ''
		return data	
		
	def get_group_user(self, iduser):
		payload = {'id': iduser}
		r = requests.get('http://ebcitakademy.alwaysdata.net/groups/user?', params=payload)
		if(r.status_code == 200):
			data = r.json()
		else:
			data = ''
		return data
		
