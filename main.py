"""
For annoying windows logins, have a simple micro that you can press a button on to send
keys down the USB, to enter your password<enter> automatically.

Bits and pieces are stolen from the adafruit_hid library, which is too big to load into
memory on the CPX (could probably compile to .mpy).

Have a password.txt file in the root dir with the password you'd like sent.
"""

from adafruit_circuitplayground.express import cpx
import time
import usb_hid


class PasswordEnterer:
    def __init__(self, pw, send_enter=True):
        self.pw = pw
        self.kbd = self.find_device(usb_hid.devices, usage_page=0x1, usage=0x06)
        self.send_enter = send_enter
        self.report = bytearray(8)
        self.empty = bytearray(8)
        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.kbd.send_report(self.empty)
        except OSError:
            time.sleep(1)
            self.kbd.send_report(self.empty)
        # Try to encode all chars so we can bomb if anything is not yet supported
        for c in self.pw:
            self.encode(c)

    def send_it(self):
        for c in self.pw:
            self.send_key(c)
        if self.send_enter:
            self.report[2] = 0x22
            self.send_report()
    
    def send_key(self, key):
        mod, keycode = self.encode(key)
        self.report[0] = mod
        self.report[2] = keycode
        self.send_report()

    def send_report(self):
        self.kbd.send_report(self.report)
        self.kbd.send_report(self.empty)

    def encode(self, c):
        """
        Hacked from adafruit's keycode file, simple way to do all letters, numbers, and
        some special characters that are likely in passwords.
        """
        if 'a' <= c <= 'z':
            return 0, 0x4 + ord(c) - ord('a')
        if 'A' <= c <= 'Z':
            return 0x2, 0x4 + ord(c) - ord('A')
        if '0' <= c <= '9':
            if c == '0':
                return 0, 0x27
            return 0, 0x1E + ord(c) - ord('1')
        if c == '\n':
            return 0, 0x28
        for i, tc in enumerate('!@#$%^&*'):
            if c == tc:
                return 0x2, 0x1E + i
        raise ValueError('Unsupported char: {}'.format(c))
        # TODO: More chars

    def find_device(self, devices, *, usage_page, usage):
        """Search through the provided list of devices to find the one with the matching usage_page and
        usage."""
        if hasattr(devices, "send_report"):
            devices = [devices]
        for device in devices:
            if (
                device.usage_page == usage_page
                and device.usage == usage
                and hasattr(device, "send_report")
            ):
                return device
        raise ValueError("Could not find matching HID device.")


with open('password.txt') as f:
    pw = f.read().strip()

try:
    enterer = PasswordEnterer(pw, send_enter=False)
except ValueError as ex:
    # Not all characters are supported yet, so indicate a bad one
    print(ex)
    cpx.red_led = True
    while True:
        time.sleep(1)
else:
    while True:
        if cpx.button_a:
            enterer.send_key('\n')
            time.sleep(.5)
            enterer.send_it()
        time.sleep(.1)

