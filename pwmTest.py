import RPi.GPIO as GPIO
import time
import os
from gps import *
import threading

GPIO.setwarnings(False)

gpsd = None #seting the global variable

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
     gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      
 
lastLatitude = 0.0
lastLongitude = 0.0


GPIO.setmode(GPIO.BCM)

pinEnable1 = 19
pinIn1 = 13
pinIn2 = 26

pinEnable2 = 18
pinIn3 = 23
pinIn4 = 24

pinEnable3 = 16
pinIn31 = 20
pinIn32 = 21

pinEnable4 = 17
pinIn41 = 27
pinIn42 = 22


GPIO.setup(pinEnable1, GPIO.OUT)
GPIO.setup(pinIn1, GPIO.OUT)
GPIO.setup(pinIn2, GPIO.OUT)

GPIO.setup(pinEnable2, GPIO.OUT)
GPIO.setup(pinIn3, GPIO.OUT)
GPIO.setup(pinIn4, GPIO.OUT)

GPIO.setup(pinEnable3, GPIO.OUT)
GPIO.setup(pinIn31, GPIO.OUT)
GPIO.setup(pinIn32, GPIO.OUT)

GPIO.setup(pinEnable4, GPIO.OUT)
GPIO.setup(pinIn41, GPIO.OUT)
GPIO.setup(pinIn42, GPIO.OUT)

GPIO.output(pinIn1, False)
GPIO.output(pinIn2, True)

GPIO.output(pinIn3, True)
GPIO.output(pinIn4, False)

GPIO.output(pinIn31, False)
GPIO.output(pinIn32, True)

GPIO.output(pinIn41, False)
GPIO.output(pinIn42, True)


p1 = GPIO.PWM(pinEnable1, 500)
p2 = GPIO.PWM(pinEnable2, 500)
p3 = GPIO.PWM(pinEnable3, 500)
p4 = GPIO.PWM(pinEnable4, 500)

p1.start(50)
p2.start(50)
p3.start(50)
p4.start(50)

lonpoint = input("Longitudinal point: ")
latpoint = input("Latitudinal point: ")

gpsp = GpsPoller() # create the thread
try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
       
        changeInLatitude = lastLatitude - gpsd.fix.latitude
        changeInLongitude = lastLongitude - gpsd.fix.longitude
        #print 'Change in Latitude  ', changeInLatitude
        #print 'Change in Latitude (M)', changeInLatitude/111200
        #print 'Change in Longitude ', changeInLongitude
        #print 'Change in Longitude (M)', changeInLongitude/111200
        lastLatitude = gpsd.fix.latitude
        lastLongitude = gpsd.fix.longitude
  

        print
        #print ' GPS reading'
        print '----------------------------------------'
        print 'latitude    ' , gpsd.fix.latitude 
        print 'longitude   ' , gpsd.fix.longitude
        print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        #print 'altitude (m)' , gpsd.fix.altitude
        #print 'eps         ' , gpsd.fix.eps
        #print 'epx         ' , gpsd.fix.epx
        #print 'epv         ' , gpsd.fix.epv
        #print 'ept         ' , gpsd.fix.ept
        print 'speed (m/s) ' , gpsd.fix.speed
        #print 'climb       ' , gpsd.fix.climb
        #print 'track       ' , gpsd.fix.track
        #print 'mode        ' , gpsd.fix.mode
        #print 'sats        ' , gpsd.satellites

        p1.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(100)
        p3.ChangeDutyCycle(100)
        p4.ChangeDutyCycle(100)

        if gpsd.fix.longitude > lonpoint:
          p1.ChangeDutyCycle(0)
          p2.ChangeDutyCycle(0)
          p3.ChangeDutyCycle(0)
          p4.ChangeDutyCycle(0)
        if gpsd.fix.latitude < latpoint:
          p1.ChangeDutyCycle(0)
          p2.ChangeDutyCycle(0)
          p3.ChangeDutyCycle(0)
          p4.ChangeDutyCycle(0)
          
        time.sleep(0.50) #set to whatever
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    p1.stop()
    p2.stop()
    p3.stop()
    p4.stop()
    GPIO.cleanup()

print "Done.\nExiting."
