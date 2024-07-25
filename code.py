
# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
from board import SCL, SDA
import busio
import time
# Import the SSD1306 module.
import adafruit_ssd1306
import board
import busio
import digitalio
from helper import MainDataHandler
from digitalio import DigitalInOut, Direction, Pull
# Create the I2C interface.
#i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
#display.fill(0)

#display.show()
# Write your code here :-)
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials UART Serial example"""


# For most CircuitPython boards:
#led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
#led.direction = digitalio.Direction.OUTPUT

#uart = busio.UART(board.TX, board.RX, baudrate=9600)


STARTING_STATE = 0
READING_STATE = 1

tmp_state = STARTING_STATE

Main_Data_Handler = MainDataHandler()
btn = digitalio.DigitalInOut(board.D13)
btn.pull = digitalio.Pull.UP

cnt = 0
Main_Data_Handler.initial_setup()
while True:
    #data = uart.read(64)  # read up to 32 bytes
    # print(data)  # this is a bytearray type
    #uart.write("No!")

    Main_Data_Handler.main_loop_call(not btn.value)



    pass
    #data = uart.read(64)  # read up to 32 bytes
    #tmp_data_string = ""
    #if data is not None:
        # convert bytearray to string
        #data_string = ''.join([chr(b) for b in data])
        #print(data_string, end="")
        #led.value = False
        #display.fill(0)
        #display.text(data_string, 0, 0, 1)
        #cnt+=1
        #display.show()


