from .Scripts import thermistor
from .Scripts import ADC0832
from .Scripts import ADC0832_2
from .Scripts import photoresistor
import RPi.GPIO as GPIO



def loop():
  while True:
    thermistor.runTemp()








if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        ADC0832_2.destroy()
        GPIO.cleanup()
        #logging.info("Stopping...")
        print ('The end !')