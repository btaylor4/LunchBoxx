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
from User import User
import places

from being_matched import BeingMatched

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
def load_user(email):
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return None
    new_user = User(email)
    new_user.db_user(user)
    return new_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    print('hit{}'.format(request.args))
    if request.method == 'POST':
        
        # routing from signup
        if(request.form['nextButton'] == 'create-profile'):
            email = request.form['email']
            password = request.form['password']
            verify_password = request.form['verify-password'] 
            
            hashed_password = generate_password_hash(password, method='sha256')
            # searches the data base for the username chosen
            requested_user = mongo.db.users.find_one({'email': email})

            if requested_user is None:
                
                if password == verify_password:    
                    # makes a new user inside data base if non already exits
                    mongo.db.users.insert({'email': email, 'password': hashed_password})
                    return render_template('create-profile.html', email=email, password=password)
                else:
                    return 'Passwords do not match'
            else:
                return 'Username has already been taken'
        
        # routing from create profile page
        elif(request.form['nextButton'] == 'done'):
            # create the user
            form = request.form
            user = User(form['email'])

            # password
            user.password = form['password']
            user.first_name = form['firstName']
            user.last_name = form['lastName']
            user.time_pref = form['lunch-time']
            user.addr = form['address']
            
            # preferences
            if('interests' in form):
                user.interest_prefs = form['interests']
            if('food' in form):
                user.food_prefs = form['food']

            # create and login user
            login_user(user)

            # redirect to the match-me page
            return redirect(url_for('user_portal'))
            
    
    return render_template('sign-up.html')


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
                return redirect(url_for('user_portal'))
            else:
                return 'Incorrect credentials.'
        else:
            return 'Incorrect email.'

    return render_template('login.html')

@app.route('/preferences', methods=['GET', 'POST'])
@login_required    
def preferences():
    if request.method == 'POST':
        food_preferences = request.form.getlist('food')
        mongo.db.being_matched.insert({'email': current_user.email, 'preferences': food_preferences, 'time_pref': current_user.time_pref })

        # TODO Return template for 'YOU'RE BEING MATCHED'

    return render_template('preferences.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/places', methods=['GET', 'POST'])
def place():
	print("I AM IN PLACE YO")
	food_type = 'italian'
	coord = (26.0895906,-80.3669549)
	resp = places.getNearbyPlaces(food_type, coord)

	print("The top restaurant is: ", resp)
	return

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/")
def index(): # TODO: Check if user is logged in
    return redirect(url_for("login"))

@app.route("/user-portal")
def user_portal():
    return render_template("user-portal.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)  # debug = true to put in debug mode
