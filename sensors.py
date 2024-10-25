import RPi.GPIO as GPIO
import time

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

def measure_distance():
    """Continuously measures and prints distance every 3 seconds."""
    print("Starting distance measurement")
    
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
                GPIO.output(LED, GPIO.HIGH)
                print("LED ON: Object detected within 5 cms")
            else:
                GPIO.output(LED, GPIO.LOW)
                print("LED OFF: No object within 5 cms")
            
            # Wait for 3 seconds before the next measurement
            time.sleep(3)

    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
