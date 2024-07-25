import board
import digitalio
import time
import board
import busio as io
from digitalio import DigitalInOut
import adafruit_ssd1306

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
oled.fill(0)
num = 0

while True:
    oled.fill(0)
    led.value = True
    time.sleep(0.01)
    led.value = False
    time.sleep(0.01)
    oled.text(str(num), 1, 20, 1)
    num = num + 1
    oled.show()
