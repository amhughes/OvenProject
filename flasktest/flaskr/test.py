
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
