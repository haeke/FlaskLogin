from flask import Flask, render_template, url_for, request, session, redirect
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from model import Base, User
app = Flask(__name__)

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
def index():
    #query the user names
    users = session.query(User).order_by(asc(User.username))
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        return render_template('index.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    users = session.query(User).order_by(asc(User.username))
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            login_session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = session.query(User).order_by(asc(User.username))
        #existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpass})
            login_session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'Username already exists'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key ='secretkey'
    app.run(debug=True)
