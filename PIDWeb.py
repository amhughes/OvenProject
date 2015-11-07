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

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
