# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import sys
import time
import RPi.GPIO as GPIO
import time
import signal
import sys


from Adafruit_BNO055 import BNO055

enable_pin = 17
in1_pin = 23
in2_pin = 24

enable_pin2 = 16
in3_pin = 27
in4_pin = 4

enable_pin3 = 6
in5_pin = 5
in6_pin = 19
########################
GPIO.setmode(GPIO.BCM)
GPIO.setup(enable_pin,GPIO.OUT)
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)

GPIO.setup(enable_pin2,GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)

GPIO.setup(enable_pin3,GPIO.OUT)
GPIO.setup(in5_pin, GPIO.OUT)
GPIO.setup(in6_pin, GPIO.OUT)

pwm = GPIO.PWM(enable_pin, 500)
pwm.start(0)

pwm2 = GPIO.PWM(enable_pin2, 500)
pwm2.start(0)

pwm3 = GPIO.PWM(enable_pin3, 500)
pwm3.start(0)
##################

def signal_handler(signal, frame):
    print("Ctrl-C pressed")
    RPi.GPIO.cleanup()
    sys.exit(0)
    
def clockwise():
	GPIO.output(in1_pin, True)
        GPIO.output(in2_pin, False)
def counter_clockwise():
        GPIO.output(in1_pin, False)
     	GPIO.output(in2_pin, True)

def clockwise2():
	GPIO.output(in3_pin, True)
        GPIO.output(in4_pin, False)
def counter_clockwise2():
        GPIO.output(in3_pin, False)
     	GPIO.output(in4_pin, True)

def clockwise3():
	GPIO.output(in5_pin, True)
        GPIO.output(in6_pin, False)
def counter_clockwise3():
        GPIO.output(in5_pin, False)
     	GPIO.output(in6_pin, True)
signal.signal(signal.SIGINT, signal_handler)

# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
# BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
# and RST connected to pin P9_12:
#bno = BNO055.BNO055(rst='P9_12')


# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
print('Reading BNO055 data, press Ctrl-C to quit...')

lastHeading = 0.0

lastRoll = 0.0

lastPitch = 0.0
while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
          heading, roll, pitch, sys, gyro, accel, mag))

    if heading > lastHeading:
        clockwise()
        pwm.ChangeDutyCycle(100)
        time.sleep(0.05)
        pwm.ChangeDutyCycle(0)
        lastHeading = heading
        print('Arm moved clockwise')
    elif heading < lastHeading:
        counter_clockwise()
        pwm.ChangeDutyCycle(100)
        time.sleep(0.05)
        pwm.ChangeDutyCycle(0)
        lastHeading = heading
        print('Arm moved counterclockwise')
    else:
        time.sleep(0.10)


    if roll > lastRoll:
        clockwise2()
        pwm2.ChangeDutyCycle(100)
        time.sleep(0.05)
        pwm2.ChangeDutyCycle(0)
        lastRoll = roll
        print('Arm moved clockwise')
    elif roll < lastRoll:
        counter_clockwise2()
        pwm2.ChangeDutyCycle(100)
        time.sleep(0.05)
        pwm2.ChangeDutyCycle(0)
        lastRoll = roll
        print('Arm moved counterclockwise')
    else:
        time.sleep(0.10)

    if pitch > lastPitch:
        clockwise3()
        pwm3.ChangeDutyCycle(100)
        time.sleep(0.05)
        pwm3.ChangeDutyCycle(0)
        lastPitch = pitch
        print('Arm moved clockwise')
    elif pitch < lastPitch:
        counter_clockwise3()
        pwm3.ChangeDutyCycle(100)
        time.sleep(0.05)
        pwm3.ChangeDutyCycle(0)
        lastPitch = pitch
        print('Arm moved counterclockwise')
    else:
        time.sleep(0.10)
    #time.sleep(0.10)
    # Other values you can optionally read:
    # Orientation as a quaternion:
    #x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    #temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    #x,y,z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    #x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    #x,y,z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    #x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    #x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.



