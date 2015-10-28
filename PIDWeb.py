from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import math
import RPi.GPIO as GPIO


DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

@app.before_request
def before_request():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    relay = GPIO.PWM(18, 0.5)
    relay.start(0)

@app.teardown_request(exception)
def teardown_request(exception):
    relay.stop()
    GPIO.cleanup()
    print('Done!')

@app.route('/')
def show_entriest():
    return render_template('show_entriest.html', Out=Out)

@app.route('/set', methods=['POST'])
def set():
    Out = request.form['Out']
    relay.ChangeDutyCycle(Out)
    flash('Set Updated')
    return redirect(url_for('show_entriest'))

#@app.route('/tune', methods=['POST'])
#def tune():
#    if not session.get('logged_in'):
#        abort(401)
#    g.db.execute('insert into entries (title,text) values (?, ?)',
#                [request.form['title'], request.form['text']])
#    g.db.commit()
#    flash('Tunings Updated')
#    return redirect(url_for('show_entries'))

#@app.route('/profile', methods=['POST'])
#def profile():
#    flash('Temperature Profile Updated')
#    return redirect(url_for('show_entries'))

#@app.route('/login', methods=['GET','POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        if request.form['username'] != app.config['USERNAME']:
#            error = 'Invalid Username'
#        elif request.form['password'] != app.config['PASSWORD']:
#            error = 'Invalid Password'
#        else:
#            session['logged_in'] = True
#            flash('You were logged in')
#            return redirect(url_for('show_entries'))
#    return render_template('login.html', error=error)

#@app.route('/logout')
#def logout():
#    session.pop('logged_in', None)
#    flash('You were logged out')
#    return redirect(url_for('show_entries'))
