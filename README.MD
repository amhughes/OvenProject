OvenPi is an oven control system built for Team PrISUm.
It is designed to use a custom PCB with a Raspberry Pi.

Built for Python 3 on flask.

Must be placed into /home/pi/OvenProject

Place the following line in the root crontab to use.

@reboot sudo python3 /home/pi/OvenProject/PIDWebv2.py >> /home/pi/PID.log 2>&1

Dependancies:
Flask (install via PIP3)

RPLCD if using the character display
