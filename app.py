from flask import Flask, render_template, url_for, request, session, redirect

from model import User
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    #query the user names
    users = session.query(User).order_by(asc(User.name))
    if 'username' not in session:
        render_template('login.html')
    else:
        return render_template('index.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    users = session.query(User).order_by(asc(User.name))
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = session.query(User).order_by(asc(User.name))
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'Username already exists'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key ='secretkey'
    app.run(debug=True)
