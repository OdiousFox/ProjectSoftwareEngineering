from network import LoRa
import socket
import time
import ubinascii
from pycoproc_1 import Pycoproc

import pycom
import machine
import ustruct

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x7f7f00) # white

# The colors of the rainbow in order.
colors = ["#cc0000", "#cc8500", "#cccc00", "#008000", "#0000cc", "#4b0082", "#ee82ee"]

## Initialise LoRa in LORAWAN mode.
# Picks the region.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# Create an OTAA authentication parameters.
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('C7470B6CCF12D08FC698C822A4712205')
dev_eui = ubinascii.unhexlify('70B3D57ED0058597')

# Join a network using OTAA (Over the Air Activation).
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# Wait until the module has joined the network.
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
# Create a LoRa socket.
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate.
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# Make the socket blocking.
# (waits for the data to be sent and for the 2 receive windows to expire).
s.setblocking(True)

## Main loop which sends the data.
while (True):

    pycom.rgbled(0x0A0A08) # White
    # Sets the current pyom board
    py = Pycoproc(Pycoproc.PYSENSE)
    # Gets pressure measurements
    mpp = MPL3115A2(py,mode=PRESSURE)
    # Gets humidty and temperature measurements
    si = SI7006A20(py)

    # Get and convert pressure to a sendable value (max 255)
    # we convert the value back in TTN
    pressure = int(mpp.pressure() * 0.01 - 900)
    # Gets the temperature
    temperature = int(si.temperature())
    # Gets the humidity
    humidity = int(si.humid_ambient(temperature))
    # Prints values out for debugging
    print("Pressure: " + str(pressure))
    print("Temperature: " + str(temperature))
    print("Humidity: " + str(humidity))
    # Packs the set values into bytes
    pressure = ustruct.pack('b', pressure)
    temperature = ustruct.pack('b', temperature)
    humidity = ustruct.pack('b', humidity)


    # Sends the packed values
    s.send(pressure + temperature + humidity)
    # Initialise a custom wait loop which sets the rgbled
    # to each color of the rainbow every 1 second 70 time.
    loop = 0
    while loop != 70:
        # loops through every color of the rainbow.
        for element in colors:
            # Get a color
            element = element[1:]
            print(element)
            # Set a color
            pycom.rgbled(int(element, 16))
            # Wait 1 second
            time.sleep(1)
        loop += 1

    # End code "Honk mi mi mi..."
