#!/bin/bash

if ! dpkg-query -s bluetooth 1> /dev/null 2>&1 ; then
    echo "Package wireless-tools is not currently installed."
    echo "--------------------------------------------------"
    echo "Install Bluetooth with:  sudo apt-get install bluetooth"
    echo "Reboot after install"
    exit 1
else
    echo "Package Bluetooth is currently installed."
fi


if [ "$1" = "mark1" ] || [ "$1" = "picroft" ]
then
    echo "Selected Mark1 or Picroft"
    source /opt/venvs/mycroft-core/bin/activate
    python /opt/mycroft/external-services/presence.py > presence.log &
elif [ "$1" = "linux" ]
then
    echo "Selected mycroft-core"
    source ~/mycroft-core/.venv/bin/activate
    python -u /opt/mycroft/external-services/presence.py > presence.log &
else
    echo "Usage: ./start-presence.sh mark1, ./start-presence.sh picroft or ./start-presence.sh linux"
fi

