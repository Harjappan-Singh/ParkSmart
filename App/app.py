from flask import Flask, render_template
import json
import RPi.GPIO as GPIO
import time
import threading

alive = 0
data = {}

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24
LED = 25

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

def main():
    measure_distance()

def turn_on_led():
    GPIO.output(LED, GPIO.HIGH)

def turn_off_led():
    GPIO.output(LED, GPIO.LOW)


def measure_distance():
    """Continuously measures and prints distance every 3 seconds."""
    print("Starting distance measurement")
    data["LED"] = False
    try:
        while True:
            GPIO.output(TRIG, False)
            print("Waiting for sensor to settle")
            time.sleep(2)
            
            # Trigger the sensor
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            # Measure pulse duration
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            
            print("Distance:", distance, "cms")

            # Check distance and control LED
            if distance < 5:
                turn_on_led()
                data["parking_space"] = 1
                print("LED ON: Object detected within 5 cms. Booked")
            else:
                turn_off_led()
                data["parking_space"] = 0
                print("LED OFF: No object within 5 cms. Available")

            if data["LED"]:
                turn_on_led()
            
            # Wait for 3 seconds before the next measurement
            time.sleep(3)

    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data["keep_alive"] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    if name == "red_led":
        if action == "on":
            data["LED"] = True
        elif action == "off":
            data["LED"] = False
    return str("ok")

if __name__ == "__main__":
    sensorsThread = threading.Thread(target=measure_distance)
    sensorsThread.start()
    app.run(host = "127.0.0.1", port = 50000, debug = True)