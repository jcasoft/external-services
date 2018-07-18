#!/bin/bash

if [ "$1" = "mark1" ] || [ "$1" = "picroft" ]
then
    echo "Selected Mark1 or Picroft"
    source /opt/venvs/mycroft-core/bin/activate
    python /opt/mycroft/external-services/webchat.py > webchat.log &
elif [ "$1" = "linux" ]
then
    echo "Selected mycroft-core"
    source ~/mycroft-core/.venv/bin/activate
    python -u /opt/mycroft/external-services/webchat.py > webchat.log &
else
    echo "Usage: ./start-webchat.sh mark1, ./start-webchat.sh picroft or ./start-webchat.sh linux"
fi

