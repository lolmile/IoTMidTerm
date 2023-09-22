#!/usr/bin/env python
import ADC0832
import time
import RPi.GPIO as GPIO

LED_PIN = 23
LIGHT_THRESHOLD = 1.65 


def init():
    ADC0832.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    

def loop():
    light_on = False  
    while True:
        res = ADC0832.getADC(1)
        vol = 3.3/255 * res
        print ('analog value: %03d  ||  voltage: %.2fV' %(res, vol))
        if vol > LIGHT_THRESHOLD:
             if not light_on:
                print("Lights ON - Alarm Triggered")
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
                light_on = True
        else:
             if light_on:
                print("Lights OFF - Alarm Closed")
                GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED
                light_on = False
        
        
        time.sleep(0.2)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print ('The end !')

