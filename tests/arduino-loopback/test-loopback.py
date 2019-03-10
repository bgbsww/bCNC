#!/bin/python2

# This script is meant to test serial loopback
# You need serial port with RX and TX shorted together
# Also you can use included arduino sketch that echoes back everything it receives
# This script sends random data and then checks if it gets received back
# If received data are different from the sent data, it reports error
# Leave this running for extended period of time to detect problems
# with wiring, EMI, chipset, etc...

import sys
import os
import serial
import time

if len(sys.argv) <= 1:
	print("Usage: %s serial_device"%(sys.argv[0]))
	exit(1)

device = sys.argv[1]

#Open arduino serial port
ser = serial.serial_for_url(device, 115200, timeout=1,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	xonxoff=False,
	rtscts=False)

#Wait for arduino to reset
#(Increase this if you have just one error in the beginning and then everything's OK)
time.sleep(2)

#Main loop
while True:
	#Send random bytes
	byte = os.urandom(64)
	ser.write(byte)
	ser.flush()

	#Receive
	received = ser.read_until(byte)

	#Compare
	if(received != byte):
		print("\nERROR!\nExpected: %s\nReceived: %s"%(byte.encode("hex"), received.encode("hex")));
