#!/usr/bin/env python
# Developed by: jcasoft
#               Juan Carlos Argueta
#


import sys
import os, time, platform
from datetime import datetime
import json

import dialog
from mycroft.configuration import Configuration
from mycroft.messagebus.client.ws import WebsocketClient
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG
from mycroft.util import create_daemon, wait_for_exit_signal


__author__ = 'jcasoft'


# ----- Variables for Websocket
configWS   = Configuration.get().get('websocket')
host       = configWS.get('host')
port       = configWS.get('port')
route      = configWS.get('route')
ssl        = configWS.get('ssl')

# ----- Variables for Proximity
configPr   = Configuration.get().get('Proximity')
proximity_enabled = configPr.get('proximity_enabled')
proximity_data_array = configPr.get('proximity_data')

# ----- Variables for Language
lang   = Configuration.get().get("lang")


ws = None

scanner_id = os.popen('uname -n').readline().strip()

devices_here = {}

AWAY_HEURISTIC = 10      # *** Can not be less than 10


# *** Get all nearby IDs
def get_bt_ids():
    sys = platform.system()
    ids = []

    f = os.popen('hcitool inq --flush')
    unparsed_data = f.readlines()[1:]
    for u in unparsed_data:
        id = u.split()[0]
        ids.append(id)
            
    return ids

# *** Scan the area for bluetooth devices. If a new device is seen, send data to messagebus.
def scan():
    time = datetime.now()
    ids = get_bt_ids()

    if (sys.version_info > (3, 0)):
        # Python 3 code in this block
        for id in ids:
            if not id in devices_here:
                send_to_messagebus({'time': time, 'device_id': id, 'scanner_id': scanner_id, 'event_type': 'ENTER'})
            devices_here[id] = time
    else:
        # Python 2 code in this block
        for id in ids:
            if not devices_here.has_key(id):
                send_to_messagebus({'time': time, 'device_id': id, 'scanner_id': scanner_id, 'event_type': 'ENTER'})
            devices_here[id] = time

# *** Clean up the list of nearby devices
def cleanup():
    del_keys = []
    time = datetime.now()
    for device in devices_here:
        last_seen = devices_here[device]
        if (time - last_seen).seconds > AWAY_HEURISTIC:
            del_keys.append(device)
            send_to_messagebus({'time': time, 'device_id': device, 'scanner_id': scanner_id, 'event_type': 'EXIT'})

    for k in del_keys:
        del devices_here[k]

def send_to_messagebus(params):
    LOG.debug('***** %s: device %s at time %s' % (params['event_type'], params['device_id'], params['time']))
    currentTime = datetime.now()
    currentTime.hour

    dialog_name = 'greeting afternoon'
    if params['event_type'] == "ENTER":
        if currentTime.hour < 12:
            dialog_name = 'greeting morning'
        elif 12 <= currentTime.hour < 19:
            dialog_name = 'greeting afternoon'
        else:
            dialog_name = 'greeting night'
    elif  params['event_type'] == "EXIT":
        dialog_name = 'bye bye'

    name = ""
    found = False
    for x in range(0,len(proximity_data_array)):
        if ("bt_id",params['device_id']) in proximity_data_array[x].items():
            name = proximity_data_array[x]["name"]
            LOG.debug("***** Devide found, Owner " + name)
            found = True
            break
        else:
            found = False

    if found:
        msg_data = {'name': name}
        payload = {'utterance':dialog.get(dialog_name, lang, msg_data)}
        ws.emit(Message("speak", payload))
    else:
        name = ""
        LOG.debug("***** Devide not found")
        msg_data = {'name': name}
        payload = {'utterance':dialog.get(dialog_name, lang, msg_data)}
        ws.emit(Message("speak", payload))



def BT_Scanner():
    LOG.debug("***** Proximity Bluetooth Enabled --> : Scanning Bluetooth devices... ")
    while True:
        # continuously scan for new devices 
        scan()
        # and clean up the list of devices that are present
        cleanup()

def main():
    global ws
    ws = WebsocketClient()
    Configuration.init(ws)

    create_daemon(ws.run_forever)

    if proximity_enabled:
        BT_Scanner()

    wait_for_exit_signal()


    
if __name__ == '__main__':
    main()


