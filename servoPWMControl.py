import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

servo_pin = 18

GPIO.setup(servo_pin, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_pin, 50)

def angle_to_duty_cycle(angle):
	return 2.5 + angle / 18.0

try:
	servo_pwm.start(angle_to_duty_cycle(45.0))
	while True:
		user_input = input("Enter 'lock', 'unlock', or 'exit' to quit: ")

		if user_input == 'lock':
			servo_pwm.ChangeDutyCycle(angle_to_duty_cycle(90.0))
			sleep(1)
		elif user_input == 'unlock':
			servo_pwm.ChangeDutyCycle(angle_to_duty_cycle(0.0))
			sleep(1)
		elif user_input == 'exit':
			servo_pwm.ChangeDutyCycle(angle_to_duty_cycle(45.0))
			print("Program Terminated.")
			break
		else:
			print("Invalid input. Enter 'lock', 'unlock', or 'exit'.")

except KeyboardInterrupt:
	servo_pwm.ChangeDutyCycle(angle_to_duty_cycle(180.0))
	print("\nProgram terminated by user.")
finally:
	GPIO.cleanup()

