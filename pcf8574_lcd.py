"""Minimal HD44780 + PCF8574 I2C backpack LCD driver for MicroPython.

Published from Open Maker Studio's own reference driver for the LCD 16x2
(I2C) Blockly block. Bit-bangs the standard "LCM1602 IIC" PCF8574 backpack
wiring used by virtually every commercial I2C LCD backpack: P0=RS, P1=RW,
P2=EN, P3=Backlight, P4-P7=D4-D7. Each expander write is its own
single-byte I2C transaction, matching real hardware where pulseEnable()
writes the byte three times (EN low, EN high, EN low).
"""


class LCD:
    def __init__(self, bus, addr, num_lines=2, num_columns=16):
        self.bus = bus
        self.addr = addr
        self.backlightval = 0x08
        self.begin()

    def _write(self, data):
        self.bus.writeto(self.addr, bytes([data | self.backlightval]))

    def _pulse(self, data):
        self._write(data | 0x04)
        self._write(data & ~0x04)

    def _write4(self, nibble, rs):
        data = (nibble << 4) | (0x01 if rs else 0x00)
        self._write(data)
        self._pulse(data)

    def _send(self, value, rs):
        self._write4((value >> 4) & 0x0F, rs)
        self._write4(value & 0x0F, rs)

    def _cmd(self, value):
        self._send(value, False)

    def putstr(self, s):
        for ch in s:
            self._send(ord(ch), True)

    def begin(self):
        self._cmd(0x28)
        self._cmd(0x0C)
        self._cmd(0x01)
        self._cmd(0x06)

    def clear(self):
        self._cmd(0x01)

    def move_to(self, col, row):
        self._cmd(0x80 | (col + (0x40 if row == 1 else 0x00)))

    def backlight_on(self):
        self.backlightval = 0x08
        self._write(0x00)

    def backlight_off(self):
        self.backlightval = 0x00
        self._write(0x00)

    def cursor_on(self):
        self._cmd(0x0E)

    def cursor_off(self):
        self._cmd(0x0C)

    def blink_on(self):
        self._cmd(0x0D)

    def blink_off(self):
        self._cmd(0x0C)
