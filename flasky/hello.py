from contextlib import redirect_stderr
from ensurepip import bootstrap
from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        r = str(self.id) + self.name
        #return '<Role %r %r>' % self.id % self.name -- syntax not working
        return r

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


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
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True

        print('aaa ' + str(session.get('known1', False)))
        print('bbb ' + str(session.get('known1', True)))
        print('ccc ' + str(session.get('known1', None)))
        print('ddd ' + str(session.get('known1')))

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    
    return render_template('index.html',current_time=datetime.utcnow(), 
        form=form, name=session.get('name'), known=session.get('known', False))

@app.route('/user/<name>') 
def user(name):
    return render_template('user.html',name=name, current_time=datetime.utcnow())

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, monment=moment)