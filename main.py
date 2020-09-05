import json
import time
from yeelight import discover_bulbs
from yeelight import Bulb


# Functions
def dance(bulb):
    print("Dancing...")

    base = 16
    multiple = (256/base)-1

    for i in range(1,2):
        print("Cycle ", i, "...")
        for j in range(0,multiple):
            bulb.set_rgb(base*(multiple-j), base*(j), 0)
            time.sleep(.25)
        for j in range(0,multiple):
            bulb.set_rgb(0, base*(multiple-j), base*(j))
            time.sleep(.25)
        for j in range(0,multiple):
            bulb.set_rgb(base*(j), 0, base*(multiple-j))
            time.sleep(.25)
    print("Cycle done")


def setFree(bulb):
    bulb.set_rgb(0, 255, 13)
    print("Set bulb to \"Free\"")

def setMeeting(bulb):
    bulb.set_rgb(5, 65, 255)
    print("Set bulb to \"Meeting\"")

def setDND(bulb):
    bulb.set_rgb(255, 31, 2)
    print("Set bulb to \"Do not disturb\"")

def printColor(blob):
    rgb = int(blob[0]["capabilities"]["rgb"])
    red = (rgb >> 16) & 0x00ff
    green = (rgb >> 8) & 0x00ff
    blue = rgb & 0x00ff
    #s = 'RGB (' + str(red) + ', ' + str(green) + ', ' + str(blue) + ')'
    #print s
    print("RGB (", red, ", ", green, ", ", blue, ")")


# MAIN

# Find bulb
print("Discovering bulbs...")
bulbs = discover_bulbs()
print("Found bulb:")
print(json.dumps(bulbs, indent=2, sort_keys=False))
ip = bulbs[0]["ip"]
#s = 'Bulb IP address: ' + ip
#print s
print()
print("'Bulb IP address: ", ip)
#printColor(bulbs)


# Get Ready
bulb = Bulb(ip)
bulb.turn_on()
bulb.set_brightness(50)
print("Ready - go check me out!")
time.sleep(10)

# Act
#dance(bulb)
setFree(bulb)
time.sleep(5)
setMeeting(bulb)
time.sleep(5)
setDND(bulb)
time.sleep(5)

# Turn off
bulb.turn_off()
