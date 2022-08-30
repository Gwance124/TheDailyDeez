#!/bin/sh
thisDir="$(dirname "$(realpath "$0")")"
cd $thisDir

echo "Starting deez bot"

if ! screen -list | grep -q "DiscordVerifier"; then
	screen -S DiscordVerifier -dm bash -c "python3.8 verifier.py"
	echo "Verifier Started"
else
	echo "Error: Verifier already running"
fi 

if ! screen -list | grep -q "MainDeezBot"; then
	screen -S MainDeezBot -dm bash -c "python3.8 main.py"
	echo "MainDeezBot Started"
else
	echo "Error: MainDeezBot already running"
fi

if ! screen -list | grep -q "DeezList"; then
	screen -S DeezList -dm bash -c "python3.8 deezList.py"
	echo "DeezList Started"
else
	echo "Error: DeezList already running"
fi
