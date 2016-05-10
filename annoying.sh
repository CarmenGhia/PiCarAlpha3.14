sudo killall gpsd
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
sudo python pwmTest.py