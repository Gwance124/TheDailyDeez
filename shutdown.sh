#!/bin/sh

thisDir="$(dirname "$(realpath "$0")")"
cd $thisDir

echo "Stopping deez bot"

if screen -list | grep -q "DiscordVerifier"; then
        screen -S DiscordVerifier -X "quit"
        echo "Verifier Stopped"
else
        echo "Error: Verifier not running"
fi

if screen -list | grep -q "MainDeezBot"; then
        screen -S MainDeezBot -X "quit"
        echo "MainDeezBot Stopped"
else
        echo "Error: MainDeezBot not running"
fi

if screen -list | grep -q "DeezList"; then
        screen -S DeezList -X "quit"
        echo "DeezList Stopped"
else
        echo "Error: DeezList not running"
fi
