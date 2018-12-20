#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class Sonar:
	
	def __init__(self, trigPin, echoPin, maxDistance):
		self.trigPin = trigPin
		self.echoPin = echoPin
		self.maxDistance = maxDistance
		self.timeOut = self.maxDistance*60
		GPIO.setmode(GPIO.BOARD) 
		GPIO.setup(self.trigPin, GPIO.OUT)   #
		GPIO.setup(self.echoPin, GPIO.IN)

	
	def pulseIn(self,pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
		t0 = time.time()
		while(GPIO.input(pin) != level):
			if((time.time() - t0) > timeOut*0.000001):
				return 0;
		t0 = time.time()
		while(GPIO.input(pin) == level):
			if((time.time() - t0) > timeOut*0.000001):
				return 0;
		pulseTime = (time.time() - t0)*1000000
		return pulseTime
		
	def getSonar(self,):     #get the measurement results of ultrasonic module,with unit: cm
		GPIO.output(self.trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
		time.sleep(0.00001)     #10us
		GPIO.output(self.trigPin,GPIO.LOW)
		pingTime = self.pulseIn(self.echoPin,GPIO.HIGH,self.timeOut)   #read plus time of echoPin
		distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
		return distance

	

