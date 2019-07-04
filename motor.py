mport RPi.GPIO as GPIO
from time import sleep
import sys, tty, termios, time
import array
GPIO.setmode(GPIO.BOARD)

Motor1A = 40
Motor1B = 38

Motor2A = 29
Motor2B = 31

MotorE = 36

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
motor1 = GPIO.PWM(40,100)
motor1.start(0)
motor1.ChangeDutyCycle(0)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
motor2 = GPIO.PWM(29,100)
motor2.start(0)
motor2.ChangeDutyCycle(0)
GPIO.setup(MotorE,GPIO.OUT)

arr=array.array('i',[60, 70, 80, 99])
i = 0
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
def motor_forward():
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(MotorE,GPIO.HIGH)

def motor_reverse():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(MotorE,GPIO.HIGH)

def motor_left():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(MotorE,GPIO.HIGH)

def motor_right():
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(MotorE,GPIO.HIGH)

def toggleSteering(direction):
    global wheelStatus

    if(direction == "right"):
        if(wheelStatus == "centre"):
            motor_right()
            motor2.ChangeDutyCycle(arr[i])
            wheelStatus = "right"
        elif(wheelStatus == "left"):
            motor1.ChangeDutyCycle(arr[i])
            wheelStatus = "centre"

    if(direction == "left"):

    if(direction == "left"):
        if(wheelStatus == "centre"):
            motor_left()
            motor1.ChangeDutyCycle(99)
            wheelStatus = "left"
        elif(wheelStatus == "right"):
            motor2.ChangeDutyCycle(0)
            wheelStatus = "centre"

GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor2A,GPIO.LOW)
GPIO.output(Motor2B,GPIO.LOW)

print("w/s: acceleration")
print("a/d: steering")
print("x: exit")

while True:

    char = getch()
   if(char == "w"):
        motor_forward()
        wheelStatus = "centre"
        motor1.ChangeDutyCycle(arr[i])
        motor2.ChangeDutyCycle(arr[i])

    if(char == "s"):
        motor_reverse()
        wheelStatus = "centre"
       motor1.ChangeDutyCycle(0)
        motor2.ChangeDutyCycle(0)

    if(char == "d"):
        toggleSteering("left")

    if(char == "a"):
        toggleSteering("right")

    if(char == "u"):
            i = 0

    if(char == "i"):
            i = 1

    if(char == "o"):
            i = 2

    if(char == "p"):
            i = 3
    if(char == "x"):
        print("Program Ended")
        break

    char = ""

GPIO.cleanup()










