import RPi.GPIO as GPIO  
import time
import json

RED_LED_PIN = 26
GREEN_LED_PIN = 16

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

def read_input_command(msg):
    if msg == "{'redLed': 'on'}":
        print("Turning on Red LED")
        turn_on_red_LED()
    elif msg == "{'redLed': 'off'}":
        print("Turning off Red LED")
        turn_off_red_LED()
    elif msg == "{'greenLed': 'on'}":
        print("Turning on Green LED")
        turn_on_green_LED()
    elif msg == "{'greenLed': 'off'}":
        print("Turning off green LED")
        turn_off_green_LED()
    elif msg == "{'parkSmartMonitor': 'on'}":
        print("Monitoring start")
    elif msg == "{'parkSmartMonitor': 'off'}":
        print("Monitoring stopped")
    else:
        print("Bad command, Try Again!!!!")


def turn_on_red_LED():
    GPIO.output(RED_LED_PIN, GPIO.HIGH)

def turn_off_red_LED():
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def turn_on_green_LED():
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

def turn_off_green_LED():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

def main():
    try:
        while True:
            try:
                user_input = input("Please specify the command: ")
                if user_input == "exit":
                    break
                else:
                    read_input_command(user_input)
            except RuntimeError as error:
                print(error.args[0])
            time.sleep(0.5)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    setup_gpio()
    main()