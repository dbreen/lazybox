# Lazybox

A very simple device that will send keystrokes via USB to enter your password/login automatically. A lot of the code was borrowed from [Adafruit's][0] [CircuitPython HID bundle][1], but tweaked to have a lower memory footprint (and less functionality).

It's currently configured for a [Circuit Playground Express][2] but it's simple to customize or add new buttons.

## How to Use

When plugged into the USB on a computer, the device will mount as an SD card. Create a password.txt file with the password you want entered when the button is pressed.

The `Enterer` class provides the functionality for sending keys, and the bottom section of the code can be customized to send various keystroke combinations, such as enter keys, with sleeps in between, etc.


[0]: https://www.adafruit.com/
[1]: https://github.com/adafruit/Adafruit_CircuitPython_HID
[2]: https://www.adafruit.com/product/3333

