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

## Try it

This guide assumes that you already configured the Arduino IDE to
use with your NodeMCU.

1. Download this repository
2. Open the credentials.c file in udpcontroller/ and edit the
   credentials to your liking
3. Open the udpcontroller program in the Arduino IDE
4. Look at the options (#defines) and set them as you want
5. Compile and flash the program
6. Use the python programs in the client folder

### blink the LED

```
$ cd client
$ python3 blinkledtest.py
```

### test the pins

```
$ cd client
$ python3 testpins.py
```

Measure the pins with a multimeter.

## Utilize the library

This is a small program showing the API.

**Note:** pins that are set as inputs are pulled up.

```python
# This program will switch the LED on when D5 is connected to GND
from nodemcu import NodeMcu, D
import time

# Connect to NodeMcu with the given IP address and port
mcu = NodeMcu(('192.168.0.206', 10000))

# Use D0 as output and D5 as input
mcu.setOutput(D[0])
mcu.setInput(D[5])

while True:
	val1, err = mcu.read(D[5])

	# handle error before interpreting value
	if err != 0:
		print(mcu.getError(err))
		break

	# val1 will be False if that pin is pulled to GND
	# and True otherwise

	# the LED on the NodeMcu will flash when D0
	# is low, so we feed it val1 and it will flash every
	# time D5 is connected to GND (e.g. by a switch)
	mcu.write(D[0], val1)
```

The truth values *True* and *False* are used to describe *HIGH* and *LOW*
states, respectively.