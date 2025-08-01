#for grab bus time
import network
import urequests
import time
from machine import Pin, I2C, SoftI2C
from pico_i2c_lcd import I2cLcd

#Connect LCD Monitor
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

#Connect WIFI By SSID
ssid = 'SSID'
password = 'PW'

#Function to connect Wifi
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        lcd.putstr('Waiting for \nconnection...\n')
        time.sleep(1)
        lcd.clear()
    ip = wlan.ifconfig()[0]
    lcd.putstr(f'Connected on \n{ip}\n')
    time.sleep(5)
    lcd.clear()
    return ip

#Function to convert time to seconds
def timestringToSec(eta):
    t = (int(eta[:4]), int(eta[5:7]), int(eta[8:10]), int(eta[11:13]), int(eta[14:16]), int(eta[17:19]), 0, 0, -1)
    secs = time.mktime( t )
    return secs

#download KMB Bus ETA
def get_bus_eta():
    #find all stop in https://data.etabus.gov.hk/v1/transport/kmb/stop/
    #68E/F
    response = urequests.get("https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/E53367ABE6927F27")
    return response

#function to break down bus eta
def show_bus_eta(api_response):
    bus_data = api_response.json()
    count = int(0)
    lcd_row = int(0)
    for bus in bus_data['data']:   
        if 'eta' in bus:
            if (bus['eta']):
                t1 = timestringToSec(bus['eta'])
                t2 = timestringToSec(bus['data_timestamp'])
                timediff= t1-t2

                #only show the bus within 30 minutes
                if(int(timediff/60)<30):
                    print(int(timediff/60))
                    print()
                    lcd.putstr(bus["route"]+" "+str(int(timediff/60))+" min \n")
                    count+=1
                    lcd_row+=1
                  
                #loop message and clear lcd monitor                
                if(lcd_row>0 and lcd_row%2==0):
                    print("lcd row "+str(lcd_row))
                    time.sleep(5)
                    lcd_row = 0
                    lcd.clear()


#main program
connect()
lcd.putstr("Start Showing\n")
lcd.putstr("Bus Arrival Time\n")
time.sleep(2)
while True:
    lcd.clear()
    show_bus_eta(get_bus_eta())
    time.sleep(5)


