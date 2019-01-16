#!/usr/bin/env python3
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO

class Handle_GPIO:
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BOARD) 
		GPIO.setup(self.pin,GPIO.OUT)
		
	def on(self):
		GPIO.output(self.pin,GPIO.HIGH)
		
	def off(self):
		GPIO.output(self.pin,GPIO.LOW)
