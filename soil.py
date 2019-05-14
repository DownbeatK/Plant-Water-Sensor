#!/usr/bin/python
# https://www.instructables.com/id/Soil-Moisture-Sensor-Raspberry-Pi/

# Library Imports
import mysql.connector as mariadb
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Database Connection
mariadb_connection = mariadb.connect(host='[IPADDRESS]', port='[PORT]', user='[USERNAME]', password='[PASSWORD]', database='[DATABASE]')
cursor = mariadb_connection.cursor()

# GPIO Setup
channel = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(channel, callback)

# 
def callback(channel):
	if GPIO.input(channel):
		print('No water' + str(GPIO.input(channel)))
		insertValue(0)
	else:
		print('Water detected' + str(GPIO.input(channel)))
		insertValue(1)

# Insert Values into DB
def insertValue(val):
	now = datetime.now()
	try:
		cursor.execute("INSERT INTO tblReadings (colDateTime, colPlant, colValue) VALUES (%s, %s , %s)", (now.strftime("%Y-%m-%d %H:%M:%S"), 1, val))
	except mariadb.Error as error:
		print("Error: {}".format(error))
	mariadb_connection.commit()

# Run Continuously
while True:
	time.sleep(1)
	
#mariadb_connection.close()