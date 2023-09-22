import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the pin numbers
BUTTON_PIN_ON = 19
BUTTON_PIN_OFF = 13
BUZZER_PIN = 25

# Set up the button and buzzer pins
GPIO.setup(BUTTON_PIN_ON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_OFF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def buzz_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzz_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    while True:
        # Check if the on button is pressed
        if GPIO.input(BUTTON_PIN_ON) == GPIO.LOW:
            buzz_on()
        # Check if the off button is pressed
        elif GPIO.input(BUTTON_PIN_OFF) == GPIO.LOW:
            buzz_off()

        # Debounce the buttons by waiting a short period of time
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up the GPIO on exit
    GPIO.cleanup()