from machine import Pin, I2C, SoftI2C
from TEA5767 import Radio
from time import sleep
from pico_i2c_lcd import I2cLcd
import _thread

#Connect Radio Module
i2c_radio = SoftI2C(scl=Pin(21), sda=Pin(20), freq=400000)
radio = Radio(i2c_radio, stereo=True,soft_mute=True, noise_cancel=True, high_cut=True)  # initialize and set to the lowest frequency
default_freq = 96.0
radio.set_frequency(default_freq)

#Connect LCD Module
i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

#Setup 2 buttons
button_up = Pin(0, Pin.IN, Pin.PULL_UP)
button_down = Pin(4, Pin.IN, Pin.PULL_UP)

#Read Radio and put info at lcd monitor
radio.read()
lcd.putstr("Radio:"+str(radio.frequency)+"\n")
lcd.putstr("Signal:"+str(radio.signal_adc_level)+"\n")


while True:
    if button_up.value() == 0:
        
        #manual mode
        radio.set_frequency(radio.frequency+0.1)
        #auto mode
        #radio.search(True, dir=1, adc=7)
        #sleep(2)
        
        radio.read()
        print('Frequency: FM {}\nReady: {}\nStereo: {}\nADC level: {}'.format(
            radio.frequency, radio.is_ready,  radio.is_stereo, radio.signal_adc_level
            ))
        
        if radio.frequency==108.0:
            radio.set_frequency(88.0)
        lcd.putstr("Radio:"+str(radio.frequency)+"   \n")
        lcd.putstr("Signal:"+str(radio.signal_adc_level)+"   \n")
        sleep(0.1)
    if button_down.value() == 0:
        
        #manual mode
        radio.set_frequency(radio.frequency-0.1)
        #auto mode
        #radio.search(True, dir=0, adc=7)
        #sleep(2)
        
        
        radio.read()
        print('Frequency: FM {}\nReady: {}\nStereo: {}\nADC level: {}'.format(
            radio.frequency, radio.is_ready,  radio.is_stereo, radio.signal_adc_level
            ))
        
        
        if radio.frequency==88.0:
            radio.set_frequency(108.0)
        lcd.putstr("Radio:"+str(radio.frequency)+"   \n")
        lcd.putstr("Signal:"+str(radio.signal_adc_level)+"   \n")
        sleep(0.1)

