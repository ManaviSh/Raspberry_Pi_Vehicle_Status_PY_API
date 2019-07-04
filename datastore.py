import smbus                    #import SMBus module of I2C
from time import sleep          #import
import serial               #import serial pacakge
import webbrowser           #import package for opening link in browser
import sys
import time
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='web', password='secretpassword', dat$

cursor = mariadb_connection.cursor()
#print("working")
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
        #write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)

        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	 #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
        #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)
	#to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
#print("working")
def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA st$
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA s$

    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\$

    lat = float(nmea_latitude)                  #convert string into float for $
    longi = float(nmea_longitude)               #convertr string into float for$

    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal$
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decima$

#convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
#print("working")

i = 0
while (i<2):
    MPU_Init()
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0

    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0
    velocity1 =Ay*0.001;
    sleep(5)

    received_data = (str)(ser.readline())                   #read NMEA string r$
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPG$
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming $
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separa$
        GPS_Info()
    i=i+1
    #print(Gx)
    readings = [
{
        'id': 1,
        'angle_x' : Gx,
        'angle_y' : Gy,
        'angle_z' : Gz,
        'acc_x' : Ax,
        'acc_y' : Ay,
        'acc_z' :Az,
        'velocity': velocity1,
        'Latitude' : lat_in_degrees,
        'Longitude' : long_in_degrees,
        'TimeStamp' : time.strftime("%c")
    }
 ]
    print(readings)
    def getReadings(amount):
#    readings = cursor.execute("SELECT TempSensor1,TempSensor2,TempSensor3,Temp$
#    mariadb_connection.commit()
       return readings

   # def addReading(reading):
    cursor.execute("INSERT INTO reading (angle_x,angle_y,angle_z,acc_x, acc_y, $
    mariadb_connection.commit()
       #return reading
#addReading(readings)
print("working")





