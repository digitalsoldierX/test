#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID 
while continue_reading:

# Scan for cards    
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

# If a card is found
	if status == MIFAREReader.MI_OK:

# Get the UID of the card
		(status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
		if status == MIFAREReader.MI_OK:
			print(uid)			
			print(status)			
			print(TagType)
			GPIO.output(35,GPIO.HIGH)
			print("%X%X%X%X" % (uid[0], uid[1], uid[2], uid[3]))
			sleep(1)
			GPIO.output(35,GPIO.LOW)
