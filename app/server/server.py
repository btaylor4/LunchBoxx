# server.py
from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_socketio import send, emit
from bson import json_util, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__, static_folder="../static", template_folder="../static")
app.config['MONGO_DBNAME'] = "lunchbox"
app.config['MONGO_URI'] = "mongodb://slackers:bigwilli3@ds263460.mlab.com:63460/lunchbox"
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"username": user_id})
    if not user:
        return None
    return User(user['_id'])

class User(object):
    def __init__(self, email):
        self.email = email
        self.password = ''
        self.first_name = ''
        self.last_name = ''
        self.interest_prefs = []
        self.food_prefs = []
        self.time_pref = ''
        self.addr = ''

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

@app.route('/register', methods=['GET', 'POST'])
def register():
    print('hit{}'.format(request.args))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        # searches the data base for the username chosen
        requested_user = mongo.db.users.find_one({'email': email})
        if requested_user is None:
            # makes a new user inside data base if non already exits
            mongo.db.users.insert(
                {'email': email, 'password': hashed_password})
            return redirect(url_for('index'))  # send back to landing page

        else:
            return 'Username has already been taken'

    return render_template('create-profile.html')


# sets up the page for registration
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        requested_user = mongo.db.users.find_one({'email': email})
        if requested_user:
            if check_password_hash(requested_user["password"], password):
                user = User(email=request.form['email'])
                login_user(user)
                return redirect(url_for('home'))
            else:
                return 'Incorrect password.'
        else:
            # return redirect(url_for('register', email=request.form['email'], password=request.form['password']))
            return 'Incorrect email.'
            
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/")
def index(): # TODO: Check if user is logged in 
    return redirect(url_for("login"))

@app.route("/user-portal")
def user_portal():
    return render_template("user-portal.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)  # debug = true to put in debug mode
