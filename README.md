# nodemcu-udp

The code in this repository will allow you to control your
NodeMCU via WiFi. That is currently limited to reading and
writing the digital pins. The client library is
implemented for python. It should be very easy
to port, though.

A controller program needs to be installed on the NodeMCU's
ESP8266 and other computers can use the client code to control the
NodeMCU via a UDP connection over WiFi.

The code is probably not fast enough for high performance controls,
but it's enough for small control processes or 
activating/deactivating peripherals remotely or based on time.

## How does it work?

The program running on the NodeMCU (*udpcontroller*) either connects
to your WiFi or opens an access point. After connecting to your WiFi
or that access point, you can use python scripts using the library in
the directory *client/* to control the NodeMCUs digital pins.
This library talks to the server on the NodeMCU via a UDP protocol
that synchronizes the state of the inputs either to or from the
NodeMCU.

### Python Library

[More information on the Python library](client/README.md)

### UDP Controller

TODO

## Try it

This guide assumes that you already configured the Arduino IDE to
use with your NodeMCU.

1. Download this repository
2. Open the credentials.c file in udpcontroller/ and edit the
   credentials to your liking
3. Open the udpcontroller program in the Arduino IDE
4. Look at the options (#defines) and set them as you want
5. Compile and flash the program
6. Use the python programs/library in the client folder 
