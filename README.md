## Mycroft Webcaht Client and Bluetooth presence service for Mycroft
Mycroft Webchat Client and Mycroft bluetooth service getting the MAC address of a Bluetooth device.


## Requirements

This code requires the bluetooth module to be installed. On Mark1, Picroft or Ubuntu/Debian systems, this can usually be done with the following commands:

    sudo apt-get install bluetooth bluez blueman

    sudo reboot now

For use with Mark1 or if you have problem with Picroft you need a [USB Bluetooth dongle ](https://www.amazon.com/Bluetooth-Dongle-Adapter-Raspberry-Windows/dp/B073H4GQ9Q/ref=sr_1_8?ie=UTF8&qid=1531953940&sr=8-8&keywords=raspberry+pi+3+usb+bluetooth+dongle) like this
![Screenshot](usb_donle.jpeg?raw=true)


## Installation

For all installations

    cd /opt/mycroft

if the installation is in Mark1 or Picroft

    sudo su mycroft

For all installations

    git clone https://github.com/jcasoft/external-services.git

if the installation is in Mark1 or Picroft

    exit

For all installations
        
    sudo chmod -R a+rwx external-services


## Installation of USB bluetooth dongle on Mark1 or if you have problem with Picroft

Plug the USB bluetooth dongle

Mark1 command line

        hciconfig -a hci1

        sudo hciconfig hci1 up

        sudo reboot now


## Configuration


Locate your configuration file and add the section detailed belove

Linux

    nano ~/.mycroft/mycroft.conf

Mark1 or Picroft

    sudo su mycroft

    nano /home/pi/.mycroft/mycroft.conf

    exit


Add this section to mycroft.conf

    "Proximity": {
        "proximity_enabled": true, 
        "proximity_data": [
            {"bt_id": "00:00:00:00:00:1A","name": "Juan Carlos"},
            {"bt_id": "00:00:00:00:00:1B","name": "Adriana"},
            {"bt_id": "00:00:00:00:00:1C","name": "Daniella"},
            {"bt_id": "00:00:00:00:00:1D","name": "Enzo"},
            {"bt_id": "00:00:00:00:00:1E","name": "Gianluca"}
        ]
    }


Fill the bt_id with bluetooth MAC address of your smart phone

![Screenshot](IOS-Bluetooth-MAC-Address.png?raw=true)

## How to start Presence service

Linux

    cd /opt/mycroft/external-services
    bash start-presence.sh linux

    cd ~/mycroft-core
    bash start-mycroft.sh debug


Mark1 or Picroft

    cd /opt/mycroft/external-services
    bash start-presence.sh mark1   
    or
    bash start-presence.sh picroft


## How to stop Presence service

Linux, Mark1 and Picroft

    cd /opt/mycroft/external-services
    bash stop-presence.sh


## How to start Webchat service

Linux

    cd /opt/mycroft/external-services
    bash start-webchat.sh linux

    cd ~/mycroft-core
    bash start-mycroft.sh debug


Mark1 or Picroft

    cd /opt/mycroft/external-services
    bash start-webchat.sh mark1
    or
    bash start-webchat.sh picroft


## How to stop Webchat service

Linux, Mark1 and Picroft

    cd /opt/mycroft/external-services
    bash stop-webchat.sh


## How to start both service

Linux

    cd /opt/mycroft/external-services
    bash start-all.sh linux

    cd ~/mycroft-core
    bash start-mycroft.sh debug


Mark1 or Picroft
    cd /opt/mycroft/external-services

    bash start-all.sh mark1
    or   
    bash start-all.sh picroft


## How to stop both services

Linux, Mark1 and Picroft

    cd /opt/mycroft/external-services
    bash stop-all.sh

## How to access Web chat from your browser

    http://localhost:9090
    or
    http://MYCROFT-IP-ADDRESS:9090


## How to use Webcaht Client and Bluetooth presence service
[![Webcaht Client and Bluetooth presence service](https://img.youtube.com/vi/J8NGy9UwkPI/0.jpg)](https://www.youtube.com/watch?v=J8NGy9UwkPI)


## Notes
Give me a Github star and follow me on YouTube !, to continue developing and improving skills and services in Mycroft

## Credits

    Author: jcasoft
            Juan Carlos Argueta


