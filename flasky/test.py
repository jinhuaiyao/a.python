from flask import Flask 
from flask import request

abc = Flask(__name__)

@abc.route('/') 
def index():
    #return '<h1>Hello World!</h1>'
    #user_agent = request.headers.get('User-Agent') 
    a = request.headers
    b = request.values
    c = request.remote_addr

    return str(c)

@abc.route('/user/<name>') 
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

