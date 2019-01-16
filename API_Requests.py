#!/usr/bin/env python3

import requests
from pprint import pprint

#http://ebcitakademy.alwaysdata.net/groups/user?

class API_Requests:
		
	def get_user(self, uid):
		payload = {'id':uid}
		r = requests.get('http://vps.quentinmodena.fr:2999/users/rfid?', params = payload)
		if(r.status_code == 200):
			data = r.json()
		else:
			data = ''
		return data	
	
	def user_authentication(self, uid):
		payload = {'id':uid}
		r = requests.post('http://vps.quentinmodena.fr:2999/records/authenticate?', params = payload)
		if(r.status_code == 200):
			data = r.json()
		else:
			data = ''
		return data
	
	def update_rfid(self, userid, uid):
		payload = {'id': userid}
		r = requests.put('http://vps.quentinmodena.fr:2999/users/update', params = payload, data = {'rfid':uid})
		data = r.json()
		return data
	
	def get_all_users(self):
		r = requests.get('http://vps.quentinmodena.fr:2999/users/all')
		if(r.status_code == 200):
			data = r.json()
		else:
			data = ''
		return data
		
