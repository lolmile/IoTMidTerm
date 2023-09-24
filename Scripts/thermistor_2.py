#!/usr/bin/env python
import ADC0832
import time
import math
import potentiometer
import RPi.GPIO as GPIO
# Define the pin numbers
BUTTON_PIN_ON = 19
BUTTON_PIN_OFF = 13
buzzer_pin = 25



def init():
  ADC0832.setup()
  GPIO.setmode(GPIO.BCM)
    # Set up the button and buzzer pins
  GPIO.setup(BUTTON_PIN_ON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BUTTON_PIN_OFF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(buzzer_pin, GPIO.OUT)
def buzz_on():
  GPIO.output(buzzer_pin, GPIO.HIGH)

def buzz_off():
  GPIO.output(buzzer_pin, GPIO.LOW)

def loop():
  potentiometer_gen = potentiometer.loop()
  buzzer_state = False
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
    if GPIO.input(BUTTON_PIN_ON) == GPIO.LOW:
      if threshold > 25:
        buzz_on()
    elif GPIO.input(BUTTON_PIN_OFF) == GPIO.LOW or threshold < 25:
        buzz_off()
    
    time.sleep(0.2)
   #CODE TO TRY TO GET THE BUTTONS TO WORK PROPERLY
  #  if GPIO.input(BUTTON_PIN_ON) == GPIO.LOW:
  #           buzzer_state = not buzzer_state
  #           time.sleep(0.2)
  #       if buzzer_state and threshold > 25:
  #           buzz_on()
  #       elif not buzzer_state or GPIO.input(BUTTON_PIN_OFF) == GPIO.LOW or threshold < 25:
  #           buzz_off()
   
   
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        GPIO.cleanup()
        #logging.info("Stopping...")
        print ('The end !')
        