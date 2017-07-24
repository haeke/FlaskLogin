from flask import Flask
from flask import flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import *

import bcrypt

engine = create_engine('sqlite:///users.db', echo=True)

app = Flask(__name__)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "You are logged in other <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    """
        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'),
        bcrypt.gensalt())
        print 'hashed: %s' % hashpass
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()

@app.route('/register', methods=['POST', 'GET'])
def register1():
    if request.method == "POST":
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
        result = query.first()
        if result:
            flash('username already exists')
        else:
            user = User(str(request.form['username']), str(request.form['password']))
            s.add(user)
            s.commit
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()

@app.route('/register', methods=['POST', 'GET'])
def register():
    return ''


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=4000)
