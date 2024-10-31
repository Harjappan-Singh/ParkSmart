import RPi.GPIO as GPIO
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import os
from dotenv import load_dotenv
import json


sensors_list = ["LED"]
data = {}

# this will replace default SubscribeListener with thing that will print out messages to console
class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f'Status: \n{status.category.name}')


load_dotenv()

config = PNConfiguration()
config.subscribe_key = os.getenv('PUBNUB_SUBSCRIBE_KEY')
config.publish_key = os.getenv('PUBNUB_PUBLISH_KEY')
config.user_id = os.getenv('PUBNUB_PI_USER_ID')

app_channel = "parksmart_pi_channel"

pubnub = PubNub(config)
pubnub.add_listener(Listener())

subscription = pubnub.channel(app_channel).subscription()

time.sleep(1)
# publish 
publish_result = pubnub.publish().channel(app_channel).message("Hello from Park Smart Pi").sync()

def handle_message(message):
    print(message.message)
   #msg = json.loads(json.dumps(message.message))
    msg = json.loads(message.message) if isinstance(message.message, str) else message.message
    if 'LED' in msg:
        print("LED status: ",msg['LED'])
        if msg['LED'] == 'on':
            data["LED"] = True
        elif msg['LED'] == 'off':
            data["LED"] = False

subscription.on_message = lambda message: handle_message(message)
subscription.subscribe()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24
LED = 25

# Setting up pins
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
    trigger = False

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
                # print("LED ON: Object detected within 5 cms")
                trigger = True
                pubnub.publish().channel(app_channel).message('"Occupied":"Yes"').sync()
                time.sleep(1)
            elif trigger:
                pubnub.publish().channel(app_channel).message('"Occupied":"No"').sync()
                turn_off_led()
                trigger = False
            # else:
            #     GPIO.output(LED, GPIO.LOW)
            #     print("LED OFF: No object within 5 cms")

            if data["LED"]:
                turn_on_led()
            
            # Wait for 3 seconds before the next measurement
            time.sleep(3)

    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
