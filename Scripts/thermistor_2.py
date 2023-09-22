#!/usr/bin/env python
import ADC0832
import time
import math
import potentiometer
import RPi.GPIO as GPIO
buzzer_pin = 25

def init():
  ADC0832.setup()
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(buzzer_pin, GPIO.OUT)
  
def buzz_on():
  GPIO.output(buzzer_pin, GPIO.HIGH)

def buzz_off():
  GPIO.output(buzzer_pin, GPIO.LOW)

def loop():
  potentiometer_gen = potentiometer.loop()
  while True:
    
    res = ADC0832.getADC(0)
    print('res', res)
    #Vr = 3.3 * res / 255
    #print("int :  ",Vr)
    Vr2 = 3.3 * float(res) / 255
    #print("float : ", Vr2, "\n")
    Rt = (10000 * 3.3 /  Vr2) - 10000
    
    #Rt = 10000 * Vr / (3.3 - Vr)
    print ('Rt : %.2f' %Rt)
    temp = 1/(((math.log(Rt / 10000)) / 3455) + (1 / (273.15+25)))
    Cel = temp - 273.15
    Fah = Cel * 1.8 + 32
    print ('Celsius: %.2f C  Fahrenheit: %.2f F' % (Cel, Fah))
    threshold = next(potentiometer_gen)
    if threshold > 25:
      buzz_on()
    else:
      buzz_off()
    
    time.sleep(0.2)
   
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        GPIO.cleanup()
        #logging.info("Stopping...")
        print ('The end !')