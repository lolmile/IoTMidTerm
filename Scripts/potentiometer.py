#!/usr/bin/env python
import ADC0832_2
import RPi.GPIO as GPIO
import time

# GPIO pin for the LED
LED_PIN = 23

 


def init():
    ADC0832_2.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    global myPWM
    myPWM = GPIO.PWM(LED_PIN, 2000)
    myPWM.start(0)
   

def loop():
    init() # Add this line
    while True:
        res = ADC0832_2.getADC(0)
        vol = 3.3/255 * res
        print ('digital value: %03d  ||  voltage: %.2fV' %(res, vol))
        DC = (res / 255)* 100
        print("DC:%03f"%(DC) )
        myPWM.ChangeDutyCycle(DC)
        time.sleep(0.2)
        yield DC
        

if __name__ == '__main__':
    init()
    
    try:
        loop()
    except KeyboardInterrupt: 
        myPWM.stop()
        ADC0832_2.destroy()
        GPIO.cleanup()
        print ('The end !')
