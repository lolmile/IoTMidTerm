import sys
sys.path.insert(0, './Scripts')
from Scripts import thermistor_2
from Scripts import ADC0832
from Scripts import ADC0832_2
import RPi.GPIO as GPIO
import subprocess


def init():
    subprocess.run(["python", "./Scripts/thermistor_2.py"])
    subprocess.run(["python", "./Scripts/buttons.py"])
def loop():

  while True:
    pass


















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
        
        
        
        