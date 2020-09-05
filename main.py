import json
import time
from yeelight import discover_bulbs
from yeelight import Bulb


print("Discovering bulbs...")
mybulb = discover_bulbs()
print(json.dumps(mybulb, indent=2, sort_keys=False))
print("Done")

bulb = Bulb("192.168.23.224")
bulb.turn_off()
print("Ready - go check me out!")
time.sleep(10)
print("Starting...")
bulb.turn_on()
bulb.set_brightness(50)

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


print("Cycle done, turning off")
bulb.turn_off()
