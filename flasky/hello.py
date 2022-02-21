from contextlib import redirect_stderr
from ensurepip import bootstrap
from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST']) 
def index():
    #return '<h1>Hello World!</h1>'
    #user_agent = request.headers.get('User-Agent') 
    #a = request.method
    #b = request.url
    #c = request.remote_addr
    #out = str(a) + "\n" + str(b) + "\n" + str(c)
    #return out
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
    
    return render_template('index.html',current_time=datetime.utcnow(), form=form, name=name)

@app.route('/user/<name>') 
def user(name):
    return render_template('user.html',name=name, current_time=datetime.utcnow())

