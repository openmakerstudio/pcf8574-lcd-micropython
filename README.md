# PCF8574 I2C LCD MicroPython Driver

Driver for a standard 16x2 (or similar) character LCD wired through a PCF8574 I2C backpack — the small blue/green board soldered onto most "I2C LCD" modules. Bit-bangs the standard "LCM1602 IIC" pin mapping (P0=RS, P1=RW, P2=EN, P3=Backlight, P4-P7=data) that virtually every commercial backpack of this type uses.

## Install

Copy `pcf8574_lcd.py` onto your board's filesystem (e.g. via [Open Maker Studio](https://openmakerstudio.com)'s Library Manager, Thonny, or `mpremote cp`).

## Usage

```python
from machine import Pin, I2C
from pcf8574_lcd import LCD

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
lcd = LCD(i2c, 0x27)  # 0x27 is the usual factory-default address

lcd.backlight_on()
lcd.putstr("Hello!")
```

## License

MIT — see [LICENSE](LICENSE).
