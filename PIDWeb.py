from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import math
import RPi.GPIO as GPIO

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
relay = GPIO.PWM(18, 0.5)
relay.start(0)

class datastore:
    def __init__(self):
        self.out = 0

dat = datastore()

@app.route('/')
def show_entriest():
    return render_template('show_entriest.html', Out=dat.out)

@app.route('/set', methods=['POST'])
def set():
    dat.out = float(request.form['out'])
    relay.ChangeDutyCycle(dat.out)
    flash('Set Updated')
    return redirect(url_for('show_entriest'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
