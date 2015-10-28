
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

#@app.before_request
#def before_request():

#@app.teardown_request(exception)
#def teardown_request(exception):

@app.route('/a')
def test1():
    return render_template('test1')

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'

