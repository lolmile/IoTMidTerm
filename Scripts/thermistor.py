#!/usr/bin/env python
import ADC0832
import time
import math

def init():
  ADC0832.setup()

def loop():
  while True:
    res = ADC0832.getADC(0)
    Vr = 3.3 * res / 255
    #print("int :  ",Vr)
    Vr2 = 3.3 * float(res) / 255
    #print("float : ", Vr2, "\n")
    Rt = (10000 * 3.3 /  Vr) - 10000
    
    #Rt = 10000 * Vr / (3.3 - Vr)
    print ('Rt : %.2f' %Rt)
    temp = 1/(((math.log(Rt / 10000)) / 3455) + (1 / (273.15+25)))
    Cel = temp - 273.15
    Fah = Cel * 1.8 + 32
    print ('Celsius: %.2f C  Fahrenheit: %.2f F' % (Cel, Fah))
    time.sleep(0.2)
   
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        logging.info("Stopping...")
        print ('The end !')


def getTemp():
  res = ADC0832.getADC(0)
  Vr = 3.3 * res / 255
  Vr2 = 3.3 * float(res) / 255
  Rt = (10000 * 3.3 /  Vr) - 10000
    
  temp = 1/(((math.log(Rt / 10000)) / 3455) + (1 / (273.15+25)))
  Cel = temp - 273.15
  Fah = Cel * 1.8 + 32
  time.sleep(0.2)

  return Cel