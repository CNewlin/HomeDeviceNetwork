# HomeDeviceNetwork
This repository is a showcase of my group's final project for the Device Networks course.

Our project was to emulate a simple network of household devices.
The devices we used include: LEDs, a temperature sensor, a heating pad, and a servo.
These are meant to mimic household appliances, such as lights, a door lock, thermostat, etc.

These are controlled via an Android app, beaglebone microcontroller, and 4 raspberry pis.
The beaglebone acts as the network hub, which connects to the app and raspberry pis. The GPIO of the pis control the devices.

The app acts as a remote, allowing the user to toggle a device with the push of a button, much like many apps available for IoT appliances we see today.

![newdiagramwoo](https://github.com/user-attachments/assets/38a82583-77d0-45ae-80a1-93a0379db25a)
![cap1](https://github.com/user-attachments/assets/fb3ba357-b1a5-49f7-9b07-274cafe88539)
