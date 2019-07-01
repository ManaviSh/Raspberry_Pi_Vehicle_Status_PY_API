import Gps_Data
import Mpu_Data
import time
import serial               #import serial pacakge
import webbrowser           #import package for opening link in browser
import sys
import smbus
import mysql.connector as mariadb
mariadb_connection = mariadb.connect(user='USERNAME', password='PASSWORD', database='weather')
cursor = mariadb_connection.cursor()



print (" Reading Data of Gyroscope and Accelerometer")

while True:
   Gps_Data.get_data()
   Mpu_Data.get_data()
    sleep(1)
    readings = [
    {	
	'id': 1,
        'angle_x' : Gx, 
        'angle_y' : Gy,
        'angle_z' : Gz,
        'acc_x' : Gx, 
        'acc_y' : Gy,
        'acc_z' : Gz,
	'velocity': velocity1,
        'Latitude' : lat_in_degrees,
        'Longitude' : long_in_degrees
        'TimeStamp' : time.strftime("%c")
    }
 ]
    def getReadings(amount):
    return readings

    def addReading(reading):
    cursor.execute("INSERT INTO reading (angle_x,angle_y,angle_z,acc_x, acc_y, acc_z,velocity,Latitude,Longitude,TimeStamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())", (reading.angle_x,reading.angle_y,reading.angle_z,reading.acc_x,reading.acc_y,reading.acc_z,reading.velocity,reading.Latitude,reading.Longitude))
    mariadb_connection.commit()
    return reading

