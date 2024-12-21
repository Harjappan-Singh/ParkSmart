import RPi.GPIO as GPIO  
import time
import json
import threading

RED_LED_PIN = 26
GREEN_LED_PIN = 16
IR_SENSOR_PIN = 25
TRIG = 23
ECHO = 24

vehicle_count = 0
monitoring_active = False
parking_triggered = False

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(IR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

# Interpret User Commands
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
        start_monitoring()
    elif msg == "{'parkSmartMonitor': 'off'}":
        print("Monitoring stopped")
        stop_monitoring()
    else:
        print("Bad command, Try Again!!!!")


# Control LEDs
def turn_on_red_LED():
    GPIO.output(RED_LED_PIN, GPIO.HIGH)

def turn_off_red_LED():
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def turn_on_green_LED():
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

def turn_off_green_LED():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)


# Monitor Vehicle Count
def monitor_vehicle_count():
    global vehicle_count, monitoring_active

    last_state = GPIO.input(IR_SENSOR_PIN)

    while monitoring_active:
        current_state = GPIO.input(IR_SENSOR_PIN)
        if last_state == 1 and current_state == 0:
            vehicle_count += 1
            print(f"Current vehicle count: {vehicle_count}")
        last_state = current_state
        time.sleep(0.1)


# Monitor Parking Space Availability
def monitor_space_availability():
    global monitoring_active, parking_triggered

    while monitoring_active:
        GPIO.output(TRIG, False)
        time.sleep(0.2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start = pulse_end = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if distance < 5 and not parking_triggered:
            parking_triggered = True
            print("{'P1': 'occupied'}")
        elif distance >= 5 and parking_triggered:
            parking_triggered = False
            print("{'P1': 'available'}")

        time.sleep(1)


# Control monitoring
def start_monitoring():
    global monitoring_active
    if not monitoring_active:
        monitoring_active = True
        threading.Thread(target=monitor_vehicle_count, daemon=True).start()
        threading.Thread(target=monitor_space_availability, daemon=True).start()

def stop_monitoring():
    global monitoring_active
    monitoring_active = False


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