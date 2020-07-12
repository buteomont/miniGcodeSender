###########################################################
## Python program to send gcode to the modified Cricut Mini
###########################################################

import sys
import serial

if len(sys.argv) < 3:
	print("\nA program to send gcode to a modified Cricut Mini.\nUsage:  python gcodeSender.py [filename] [usb port]\n")
	exit(1)
	
	
## get the filename and the serial port from the command line
filename = sys.argv[1]
usbport = sys.argv[2]


# configure the serial connection
ser = serial.Serial(
    port=usbport,
    baudrate=115200
)

# Function to process a line by sending it to the cutter and 
# wait for the response
def cutter(gcodeLine):
	if gcodeLine=='' or gcodeLine[0]=="(" or gcodeLine[0]=="%":
		return
	print(">> "+gcodeLine)
	
	# send the line to the cutter
	ser.write((gcodeLine+'\r\n').encode())
	resp = str(ser.readline().decode('utf-8')).strip() # response looks weird without the decode() call
	if resp != '':
		print("<< " + resp)
	if resp != "ok":
		print("\nBad return code '"+resp+"'. Try resetting the cutter. Exiting.")
		ser.close()
		exit(2)
		
##read the file into an array
with open(filename) as f:
	lines = f.readlines()

for line in lines:
	cutter(line.strip())


