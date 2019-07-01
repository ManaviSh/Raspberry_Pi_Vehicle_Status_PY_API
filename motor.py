import RPi.GPIO as io
io.setmode(io.BCM)
import sys, tty, termios, time
import array
import Mpu_Data

motor1_in1_pin = 6
motor1_in2_pin = 5
io.setup(motor1_in1_pin, io.OUT)
io.setup(motor1_in2_pin, io.OUT)
motor1 = io.PWM(6,100)
motor1.start(0)
motor1.ChangeDutyCycle(0)

motor2_in1_pin = 20
motor2_in2_pin = 21
io.setup(motor2_in1_pin, io.OUT)
io.setup(motor2_in2_pin, io.OUT)
motor2 = io.PWM(20,100)
motor2.start(0)
motor2.ChangeDutyCycle(0)

brr=array.array('j',[10,20,30,40,50,60,70,80,90])
arr=array.array('i',[70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,90,91])
policy=[0, 33, 31, 33, 32, 26, 30, 27, 32, 30, 31, 30, 34, 28, 29, 14, 29, 17, 1, 2, 1, 0, 1, 0, 0, 1, 2, 1, 0, 1, 1, 1]

j = 0
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
    io.output(motor1_in1_pin, True)
    io.output(motor1_in2_pin, False)
    io.output(motor2_in1_pin, True)
    io.output(motor2_in2_pin, False)

def motor_reverse():
    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, True)
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, True)

def motor_left():
    io.output(motor1_in1_pin, True)
    io.output(motor1_in2_pin, False)    
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, False)

def motor_right():
    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, False)    
    io.output(motor2_in1_pin, True)
    io.output(motor2_in2_pin, False)

def motor_stop():
    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, False)    
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, False)
	
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
        if(wheelStatus == "centre"):
            motor_left()
            motor1.ChangeDutyCycle(99)
            wheelStatus = "left"
        elif(wheelStatus == "right"):
            motor2.ChangeDutyCycle(0)
            wheelStatus = "centre"


def angleanalyser():
    angle = Mpu_Data.Gx
    k = abs(angle)
    z = k/0.104562
    if(angle < 0):
        m = 15-z
    else:
        m = 16+z
    r = m%i
    i= m-r

io.output(motor1_in1_pin, False)
io.output(motor1_in2_pin, False)
io.output(motor2_in1_pin, False)
io.output(motor2_in2_pin, False)

wheelStatus = "centre"

print("w: increase velocity")
print("s: stop")
print("r: reverse")
print("a/d: steering")
print("x: exit")

while True:

    char = getch()
    angleanalyser()
    if(char == "w"):
        motor_forward()
        if(j<10):
            j = j+1
        wheelStatus = "centre"
        if(brr[j]<(arr[i]+1) and brr[j]>(arr[i]-1)):
            v=brr[j]
        else:
            v=arr[i]
        motor1.ChangeDutyCycle(v)
        motor2.ChangeDutyCycle(v)

    if(char == "r"):
        motor_reverse()
        j=0
        wheelStatus = "centre"
        motor1.ChangeDutyCycle(0)
        motor2.ChangeDutyCycle(0)

    if(char == "s"):
        motor_stop()
        j=0

    if(char == "a"):
        toggleSteering("left")

    if(char == "d"):
        toggleSteering("right")

    if(char == "x"):
        print("Program Ended")
        break
    u = Mpu_Data.velocity1
    angleanalyser()
    if ((u<(policy(i)+5)):
        print("Increase speed for maximum range")
    elif ((u>(policy(i)+5)):
        print("Decrease speed for maximum range")

    char = ""

io.cleanup()
