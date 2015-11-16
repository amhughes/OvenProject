from flask import Flask, request, session, redirect, url_for, \
     abort, render_template, flash
import math
import RPi.GPIO as GPIO
from time import perf_counter
import threading

tunefile = open('data/tunings.txt', 'r')
kpt= tunefile.readline()
kit= tunefile.readline()
kdt= tunefile.readline()
tunefile.close()

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

class datastore:
    def __init__(self, kpti, kiti, kdti):
        self.kp = float(kpti[4:-2])
        self.ki = float(kiti[4:-2])
        self.kd = float(kdti[4:-2])
        self.sp = 100
        self.Out = 0
        self.T = 0
        self.timel = []
        self.spl = []
        self.Outl = []
        self.TL = []
        self.kill = True
        self.status = 'Off'
    def record(self):
        self.TL.append(self.T)
        self.Outl.append(self.Out)

class PIDloop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        dat.kill = False
        timold = perf_counter()
        Told = thermocouple.get()
        outMin = 0
        outMax = 0
        interr = 0
        while not(dat.kill):
            tim = perf_counter()
            if (tim-timold)>1:
                timold = tim
                dat.T = thermocouple.get()
                Trj = thermocouple.get_rj()
                if dat.T < (Trj-10): break
                err = dat.sp - dat.T
                interr += dat.ki*err
                if interr > outMax:
                    interr = outMax
                elif interr < outMin:
                    interr = outMin
                din = dat.T - Told
                dat.Out = dat.kp*err + interr - dat.kd*din
                if dat.Out > outMax:
                    dat.Out = outMax
                elif dat.Out < outMin:
                    dat.Out = outMin
                print(dat.T)
                print(dat.sp)
                print(dat.Out)
                relay.ChangeDutyCycle(dat.Out)
                Told = dat.T

class RampLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        tmin = 0
        timoldr = perf_counter()
        dat.record()
        while not(dat.kill):
            timr = perf_counter()
            if (timr-timoldr)>60:
                timoldr = timr
                tmin += 1
                dat.record()
                if len(dat.TL) == len(dat.spl):
                    dat.kill = True
                    dat.status = 'Complete'
                    break
                dat.sp = dat.spl[tmin]

@app.before_request
def before_request():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    relay = GPIO.PWM(18, 0.5)
    relay.start(0)
    dat = datastore(kpt, kit, kdt)
    cs_pin = 8
    clock_pin = 11
    data_pin = 9
    units = 'f'
    thermocouple = MAX31855(cs_pin, clock_pin, data_pin, units)
    PIDloopT = PIDloop()
    RampLoopT = RampLoop()

@app.teardown_request(exception)
def teardown_request(exception):
    relay.stop()
    GPIO.cleanup()
    print('Done!')

@app.route('/')
def main():
    return render_template('main.html', Out=dat.Out, Status=dat.status)

@app.route('/preheat', methods=['POST'])
def preheat():
    dat.sp = 100
    PIDloopT.start()
    flash('Preheat Enabled')
    dat.status = 'PreheatNP'
    return redirect(url_for('main'))

@app.route('/startrun', methods=['POST'])
def startrun():
    flash('Run Started')
    dat.status = 'Run'
    return redirect(url_for('main'))

@app.route('/kill', methods=['POST'])
def kill():
    dat.kill = True
    flash('Run Stopped')
    dat.status = 'Off'
    return redirect(url_for('main'))

@app.route('/tune', methods=['POST'])
def tune():
    if not session.get('logged_in'):
        abort(401)
    dat.kp = float(request.form['kp'])
    dat.ki = float(request.form['ki'])
    dat.kd = float(request.form['kd'])
    tunefile = open('data/tunings.txt', 'w')
    tunefile.write(('kp=' + str(dat.kp) + '\nki=' + str(dat.ki) + '\nkd=' + str(dat.kd) + '\n'))
    tunefile.close()
    flash('Tunings Updated')
    return redirect(url_for('main'))

@app.route('/profile', methods=['POST'])
def profile():
    RunName = request.form['Name']
    HoldT = float(request.form['HoldT'])
    HoldTim = float(request.form['HoldTim'])
    UR = float(request.form['UR'])
    DR = float(request.form['DR'])
    opf = open('schedule.txt', 'w')
    opf.write('Time      SP\n')
    i = 0
    sploc = dat.sp
    dat.timel.append(i)
    dat.spl.append(sploc)
    opf.write(str(dat.timel[i]) + ' ' + str(dat.spl[i]) + '\n')
    while dat.spl[i] + UR < HoldT:
        i += 1
        sploc += UR
        dat.spl.append(sploc)
        dat.timel.append(i)
        opf.write(str(dat.timel[i]) + ' ' + str(dat.spl[i]) + '\n')
    else:
        i += 1
        sploc = HoldT
        dat.spl.append(sploc)
        dat.timel.append(i)
        opf.write(str(dat.timel[i]) + ' ' + str(dat.spl[i]) + '\n')
    for j in range(HoldTim):
        i += 1
        dat.spl.append(sploc)
        dat.timel.append(i)
        opf.write(str(dat.timel[i]) + ' ' + str(dat.spl[i]) + '\n')
    while dat.spl[i] > dat.sp:
        i += 1
        sploc -= DR
        dat.spl.append(sploc)
        dat.timel.append(i)
        opf.write(str(dat.timel[i]) + ' ' + str(dat.spl[i]) + '\n')
    opf.close()
    dat.status = 'PreheatP'
    flash('Temperature Profile Updated')
    return redirect(url_for('main'))

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