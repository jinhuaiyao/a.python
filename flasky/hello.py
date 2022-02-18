from contextlib import redirect_stderr
from ensurepip import bootstrap
from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/') 
def index():
    #return '<h1>Hello World!</h1>'
    #user_agent = request.headers.get('User-Agent') 
    #a = request.method
    #b = request.url
    #c = request.remote_addr
    #out = str(a) + "\n" + str(b) + "\n" + str(c)
    #return out
    return render_template('index.html')

@app.route('/user/<name>') 
def user(name):
    return render_template('user.html',name=name)

