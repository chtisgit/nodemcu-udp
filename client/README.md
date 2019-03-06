# nodemcu python lib

## Usage

This is a small program showing the API.

**Note:** pins that are set as inputs are pulled up.

```python
#!/usr/bin/python3

# In this example the LED on the NodeMCU board can be toggled
# by a button connecting D1 to GND.

from nodemcu import NodeMcu, NodeMcuError, D
from time import sleep
from sys import exit
from common import getIPPort

try:
	mcu = NodeMcu(getIPPort())
	mcu.setOutput(D[0])
	mcu.setInput(D[1])

	print("Press button on D1 to toggle LED")
	bit = False
	changeOk = True

	while True:
		mcu.write(D[0], bit)

		n = mcu.read(D[1])

		# when the button is pressed n == False
		if n == False and changeOk:
			# only toggle the led when the button has been released since the last change
			bit = not bit
			changeOk = False
		elif n == True:
			# when the button is released, allow the user to toggle the LED again
			changeOk = True

except NodeMcuError as e:
	print("error:", e)
```

The truth values *True* and *False* are used to describe *HIGH* and *LOW*
states, respectively.

## Examples

### Test the pins

```
$ cd client
$ python3 example_test_pins.py 192.168.x.y
```

Measure the pins with a multimeter or wire LEDs to them.

### Blink the LED

```
$ cd client
$ python3 example_blink_led.py 192.168.x.y
```

### Toggle the LED with a button

```
$ cd client
$ python3 example_led_button.py 192.168.x.y
```

Pressing the button turns the LED off if turned on and vice-versa.

![example_led_button](https://user-images.githubusercontent.com/9674768/53916688-15037980-4063-11e9-9ba0-981298bcdda5.gif)

### Use a 7 segment display

```
$ cd client
$ python3 example_7seg_display.py 192.168.x.y
```

This example needs a bit more complex wiring. It also uses a 74HC595 shift register. The image below shows the display counting from 0 to 9. Unfortunately, one of the segments was not properly connected by the breadboard.

![example_7seg_display](https://user-images.githubusercontent.com/9674768/53916686-146ae300-4063-11e9-824e-426752028501.gif)
