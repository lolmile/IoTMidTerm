#!/usr/bin/env python
import ADC0832
import time
import math
from time import sleep
import smbus
import potentiometer
import RPi.GPIO as GPIO
# Define the pin numbers
BUTTON_PIN_ON = 19
BUTTON_PIN_OFF = 13
buzzer_pin = 25


LED_PIN = 23
LIGHT_THRESHOLD = 1.65 



#code for the screen 

def delay(time):
    sleep(time/1000.0)

def delayMicroseconds(time):
    sleep(time/1000000.0)


class Screen():

    enable_mask = 1<<2
    rw_mask = 1<<1
    rs_mask = 1<<0
    backlight_mask = 1<<3

    data_mask = 0x00

    def __init__(self, cols = 16, rows = 2, addr=0x27, bus=1):
        self.cols = cols
        self.rows = rows        
        self.bus_num = bus
        self.bus = smbus.SMBus(self.bus_num)
        self.addr = addr
        self.display_init()
        
    def enable_backlight(self):
        self.data_mask = self.data_mask|self.backlight_mask
        
    def disable_backlight(self):
        self.data_mask = self.data_mask& ~self.backlight_mask
       
    def display_data(self, *args):
        self.clear()
        for line, arg in enumerate(args):
            self.cursorTo(line, 0)
            self.println(arg[:self.cols].ljust(self.cols))
           
    def cursorTo(self, row, col):
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.command(0x80|(offsets[row]+col))
    
    def clear(self):
        self.command(0x10)

    def println(self, line):
        for char in line:
            self.print_char(char)     

    def print_char(self, char):
        char_code = ord(char)
        self.send(char_code, self.rs_mask)

    def display_init(self):
        delay(1.0)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(0.15)
        self.write4bits(0x20)
        self.command(0x20|0x08)
        self.command(0x04|0x08, delay=80.0)
        self.clear()
        self.command(0x04|0x02)
        delay(3)

    def command(self, value, delay = 50.0):
        self.send(value, 0)
        delayMicroseconds(delay)
        
    def send(self, data, mode):
        self.write4bits((data & 0xF0)|mode)
        self.write4bits((data << 4)|mode)

    def write4bits(self, value):
        value = value & ~self.enable_mask
        self.expanderWrite(value)
        self.expanderWrite(value | self.enable_mask)
        self.expanderWrite(value)        

    def expanderWrite(self, data):
        self.bus.write_byte_data(self.addr, 0, data|self.data_mask)

#end of code for screen

#code for the other components

def init():
  ADC0832.setup()
  GPIO.setmode(GPIO.BCM)
    # Set up the button and buzzer pins
  GPIO.setup(BUTTON_PIN_ON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BUTTON_PIN_OFF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(buzzer_pin, GPIO.OUT)
  GPIO.setup(LED_PIN, GPIO.OUT)
  GPIO.output(LED_PIN, GPIO.LOW)  # Turn on the LED
  
def buzz_on():
  GPIO.output(buzzer_pin, GPIO.HIGH)

def buzz_off():
  GPIO.output(buzzer_pin, GPIO.LOW)

def loop():
  potentiometer_gen = potentiometer.loop()
  buzzer_state = False
  
  light_text = "Dark" 
  screen = Screen(bus=1, addr=0x27, cols=16, rows=2)
 
  screen.enable_backlight() 
  while True:
    
    res = ADC0832.getADC(0)
    #print('res', res)
    #Vr = 3.3 * res / 255
    #print("int :  ",Vr)
    
    Vr2 = 3.3 * float(res) / 255
   # print("float : ", Vr2, "\n")
    Rt = (10000 * 3.3 /  Vr2) - 10000
    
    #Rt = 10000 * Vr / (3.3 - Vr)
   # print ('Rt : %.2f' %Rt)
    temp = 1/(((math.log(Rt / 10000)) / 3455) + (1 / (273.15+25)))
    Cel = temp - 273.15
    Fah = Cel * 1.8 + 32
   # print ('Celsius: %.2f C  Fahrenheit: %.2f F' % (Cel, Fah))
    threshold = next(potentiometer_gen)
   # print("threshold", threshold)
   #CODE TO TRY TO GET THE BUTTONS TO WORK PROPERLY
    if GPIO.input(BUTTON_PIN_ON) == GPIO.LOW:
              buzzer_state = True
              time.sleep(0.1)
    if GPIO.input(BUTTON_PIN_OFF) == GPIO.LOW:
              buzzer_state = False
              time.sleep(0.1)
    if buzzer_state:
      if  Cel > threshold:
        buzz_on()
      else:
        buzz_off()
    else:
       buzz_off()
    
    res2 = ADC0832.getADC(1)
    vol = 3.3/255 * res2
        
    print ('analog value: %03d  ||  voltage: %.2fV' %(res2, vol))
    if vol < LIGHT_THRESHOLD:
          
        print("Dark")
        light_text = "Dark" 

        print("Lights OFF - Alarm Closed")
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
    
    else:
          print("Light")
          light_text = "Light" 
          print("Lights ON - Alarm Triggered")
          GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED
            
    
    line1 = 'C:%.1f Set:%.1fC' % (Cel, threshold )
    line2 = 'Room: %s' % (light_text)
    screen.display_data(line1, line2)
          
           
       
    
    
       
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
        