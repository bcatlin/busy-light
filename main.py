#!/usr/local/bin/python3

# General libs
from __future__ import print_function
import sys
import json
import time
import datetime
import pickle
import os.path
import argparse

# Yeelight libs
from yeelight import discover_bulbs
from yeelight import Bulb

# Google Calendar libs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Color Constants
FREE_RED = 0
FREE_GREEN = 255
FREE_BLUE = 13
FREE_RGB = (FREE_RED << 16) | (FREE_GREEN << 8) | FREE_BLUE
MEETING_RED = 5
MEETING_GREEN =65 
MEETING_BLUE = 255
MEETING_RGB = (MEETING_RED << 16) | (MEETING_GREEN << 8) | MEETING_BLUE
DND_RED = 255
DND_GREEN = 31
DND_BLUE = 2
DND_RGB = (DND_RED << 16) | (DND_GREEN << 8) | DND_BLUE


def printUsageAndExit():
    print("Usage:")
    print(" ", sys.argv[0], "[free|meeting|dnd|off]     -- Set bulb to specified scene.")
    print("  Note: Calling with no arguments executes test code.")
    exit(-1)


##########################################################################
# Bulb Functions
##########################################################################
def getBulbs():
    print("Discovering bulbs...")
    bulbs = discover_bulbs()
    #print("Found bulb:")
    #print(json.dumps(bulbs, indent=2, sort_keys=False))
    return bulbs

def printBulbStatus(bulb):
    print("\n##################################")
    props = bulb.get_properties()

    # Power State
    print('# Power State:   ' + props["power"])

    # Color
    rgb = int(props["rgb"])
    red = (rgb >> 16) & 0x00ff
    green = (rgb >> 8) & 0x00ff
    blue = rgb & 0x00ff
    print('# RGB Value:     (' + str(red) + ', ' + str(green) + ', ' + str(blue) + ')')

    scene = "(unknown)"
    if rgb == FREE_RGB:
        scene = "\"Free\""
    elif rgb == MEETING_RGB:
        scene = "\"Meeting\""
    elif rgb == DND_RGB:
        scene = "\"Do not Disturb\""
    print('# Scene:         ' + scene)

    print("##################################")

def setFree(bulb):
    bulb.turn_on()
    bulb.set_rgb(FREE_RED, FREE_GREEN, FREE_BLUE)
    print("Set bulb to \"Free\"")

def setMeeting(bulb):
    bulb.turn_on()
    bulb.set_rgb(MEETING_RED, MEETING_GREEN, MEETING_BLUE)
    print("Set bulb to \"Meeting\"")

def setDND(bulb):
    bulb.turn_on()
    bulb.set_rgb(DND_RED, DND_GREEN, DND_BLUE)
    print("Set bulb to \"Do not disturb\"")

def setOff(bulb):
    setFree(bulb)
    bulb.turn_off()
    print("Turned bulb off")

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


##########################################################################
# Google Calendar Functions
##########################################################################

def getGCalService():
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # NOTE: If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


##########################################################################
# MAIN
##########################################################################

#print("Number of arguments: ", len(sys.argv), " arguments.")
#print("Argument List: ", str(sys.argv))

# Usage
parser = argparse.ArgumentParser(description='Manage your Yeelight as a busy light.')
parser.add_argument('--status', help='Print status', action='store_true')
parser.add_argument('--set', help='Set new scene', action='store', choices=["free", "meeting", "dnd", "off"])
# Parse Args
args = parser.parse_args()

# Initialize
bulbs = getBulbs()
print("Total bulbs: ", len(bulbs))
ip = bulbs[0]["ip"]
print("Bulb IP (first bulb): ", ip)
bulb = Bulb(ip)

if args.set:
    if args.set == "free":
        setFree(bulb)
    elif args.set == "meeting":
        setMeeting(bulb)
    elif args.set == "dnd":
        setDND(bulb)
    elif args.set == "off":
        setOff(bulb)
if args.status:
    printBulbStatus(bulb)

print("\n\nEXITING....\n\n")
exit(0)

if (len(sys.argv) == 2):
    # Initialize
    ip = getBulbIP()
    bulb = Bulb(ip)

    if (sys.argv[1] == "free"):
        setFree(bulb)
    elif (sys.argv[1] == "meeting"):
        setMeeting(bulb)
    elif (sys.argv[1] == "dnd"):
        setDND(bulb)
    elif (sys.argv[1] == "off"):
        bulb.turn_off()
    else:
        printUsageAndExit()
    exit(0)


# TEST CODE

# Call the Calendar API
service = getGCalService()

print('Getting Google Calendar list...')
callist_result = service.calendarList().list(maxResults=50, showDeleted=False, showHidden=False).execute()
callist = callist_result.get('items', [])

print('Google Calendars:')
if not callist:
    print('* No calendars found.')
for cal in callist:
    print(cal['summary'], "(", cal['kind'], ")")

exit(0)





"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""

now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

exit(0)


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
