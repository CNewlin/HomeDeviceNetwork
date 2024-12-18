import socket
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT


# Define GPIO pin for LED
sensor = Adafruit_DHT.DHT11
pin = 4
pad_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(pad_pin, GPIO.OUT)
# Define the server's IP address and port
server_ip = "host ip"
server_port = 4020

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

    # Connect to the server
    client_socket.connect((server_ip, server_port))
    message = "Temperature Connected"
    client_socket.send(message.encode("utf-8"))
    message = "Temperature Off"
    client_socket.send(message.encode("utf-8"))
    message = ""
    print("Connected to the server on {}:{}".format(server_ip, server_port))

    while True:
        temperature = "None"
        humidity = "None"

        # Receive data from the server
        data = client_socket.recv(1024)  # You can adjust the buffer size as ne>

        if not data:
            print("Server disconnected")
            break

        # Process the received data
        received_message = data.strip()
        if received_message.decode() != "off":
           while str(temperature) == 'None':
              GPIO.output(pad_pin, 1)
              humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
              sleep(1)
              message = "TM" + str(temperature) + "HM" + str(humidity)

           client_socket.send(message.encode("utf-8"))
           message = ""
           print("Received message: {}".format(received_message))
        elif received_message.decode() == "off":
           GPIO.output(pad_pin, 0)
           print("Received Off!")
           break

except ConnectionRefusedError:
    print("Connection to the server failed. Ensure the server is running and re>
except KeyboardInterrupt:
    print("Client closed by the user.")
finally:
    # Close the client socket when done
    client_socket.close()