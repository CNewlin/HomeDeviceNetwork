from gpiozero import LED
from time import sleep

red_led = LED(19)
green_led = LED(26)

try:
	while True:
		user_input = input("Enter 'red' to turn red on, 'green' to turn green on, 'off' to turn both off, or 'exit' to quit: ")

		if user_input == 'red':
			red_led.on()
			green_led.off()
		elif user_input == 'green':
			green_led.on()
			red_led.off()
		elif user_input == 'off':
			red_led.off()
			green_led.off()
		elif user_input == 'exit':
			red_led.off()
			green_led.off()
			print("Program terminated.")
			break
		else:
			print("Invalid input. Enter 'red','green' or 'exit'.")

except KeyboardInterrupt:
	red_led.off()
	green_led.off()
	print("\nProgram terminated by user.")

