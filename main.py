# main.py -- put your code here!
import time
from pysense import Pysense
import pycom
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import os
import urequests
from network import WLAN


pycom.heartbeat(False)


py = Pysense()

mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
print("MPL3115A2 temperature: " + str(mp.temperature()))
print("Altitude: " + str(mp.altitude()))
mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
print("Pressure: " + str(mpp.pressure()))

si = SI7006A20(py)
print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")
t_ambient = 24.4
print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

lt = LTR329ALS01(py)
print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

li = LIS2HH12(py)
print("Acceleration: " + str(li.acceleration()))
print("Roll: " + str(li.roll()))
print("Pitch: " + str(li.pitch()))
print("Battery voltage: " + str(py.read_battery_voltage()))

def sendSignal():
    while True:
        pycom.rgbled(0x0000FF) # white
        pybytes.send_battery_level(int(py.read_battery_voltage()))
        pybytes.send_signal(1,si.temperature())
        pybytes.send_signal(2,si.humidity())
        pybytes.send_signal(3,mpp.pressure())
        pybytes.send_signal(4,lt.light()[0])
        pycom.rgbled(0x0) # off
        time.sleep(30)

#add code to send an sms message

#add code to store sensor data in an no-sql database


#send notification via email of the temperature
def send_email_notification():
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(ssid="Jordan Erifried's iPhone", auth=(WLAN.WPA2, "Jordan2002"))
    if not wlan.isconnected():
        print('looking for network....')
        wlan.connect(ssid="Jordan Erifried's iPhone", auth=(WLAN.WPA2, "Jordan2002"))
        while not wlan.isconnected():
            machine.idle()
    print("WiFi connected succesfully")
    print(wlan.ifconfig())#see other available routers
    response = urequests.post("http://cow.flcl.co:3000/email", data = "danerifried@gmail.com" + "  " +  str(si.temperature()) + "")
    #response = urequests.post("http://cow.flcl.co:3000/sms", data = "+250782330752" + "  " +  str(t_ambient) + "")
    response.close()
send_email_notification()
sendSignal()
