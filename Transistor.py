#!/usr/bin/env python3
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO

class Transistor:
	def __init__(self, pin):
		self.pin = pin
		GPIO.setmode(GPIO.BOARD) 
		GPIO.setup(self.pin,GPIO.OUT)
		self.off()
		
	def on(self):
		GPIO.output(self.pin,GPIO.HIGH)
		
	def off(self):
		GPIO.output(self.pin,GPIO.LOW)
