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
import datetime
from time import time

from matching_algorithm import form_groups

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
                    if(len(password) > 5):
                        # makes a new user inside data base if non already exits
                        mongo.db.users.insert({'email': email, 'password': hashed_password})
                        return render_template('create-profile.html', email=email, password=password, hidden='hidden')
                    else:
                        return render_template('sign-up.html', error='Passwords must be at least 6 characters.')
                else:
                    return render_template('sign-up.html', error='Passwords do not match.')
            else:
                return render_template('sign-up.html', error='Username has already been taken.')

        # routing from create profile page
        elif(request.form['nextButton'] == 'done'):
            # create the user
            form = request.form

            email = form['email']
            password = form['password']

            user = User(email)


            print('form[\'lunch-time\']:', form['lunch-time'])

            now = datetime.datetime.utcnow()

            print('now:', now)

            tempTimeString = now.strftime("%d%m%Y") + " " + form['lunch-time']

            print('tempTimeString:', tempTimeString)

            tempTime = datetime.datetime.strptime(tempTimeString, "%d%m%Y %I:%M %p")

            print('tempTime:', tempTime)

            timeDiff = (tempTime-datetime.datetime(1970,1,1)).total_seconds()

            print('timeDiff:',timeDiff)

            user.first_name = form['firstName']
            user.last_name = form['lastName']
            user.time_pref = round(timeDiff)
            user.addr = form['address']

            # handle errors
            if(user.first_name == ''):
                return render_template('create-profile.html', email=email, password=password, error='First name can not be empty.')
            elif(user.last_name == ''):
                return render_template('create-profile.html', email=email, password=password, error='Last name can not be empty.')
            elif(user.addr == ''): # TODO: see if address exits (google maps)
                return render_template('create-profile.html', email=email, password=password, error='Address is invalid.')

            # preferences
            if('interests' in form):
                user.interest_prefs = form.getlist('interests')
            if('food' in form):
                user.food_prefs = form.getlist('food')
            update = {'first_name':user.first_name, 'last_name':user.last_name, 'time_pref':user.time_pref, 'addr':user.addr, 'interest_prefs':user.interest_prefs, 'food_prefs':user.food_prefs}

            # find and update user
            mongo.db.users.update_one({'email': user.email}, {'$set': update})


            # redirect to the login page
            return redirect(url_for('login'))


    return render_template('sign-up.html', hidden='hidden')


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
        return render_template('login.html', error='Incorrect username or password.')

    return render_template('login.html', hidden='hidden')

@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':

        now = datetime.datetime.utcnow()
        tempTimeString = now.strftime("%d%m%Y") + " " + request.form['lunch-time']
        tempTime = datetime.datetime.strptime(tempTimeString, "%d%m%Y %I:%M %p")
        timeDiff = (tempTime-datetime.datetime(1970,1,1)).total_seconds()

        mongo.db.being_matched.insert({'email': current_user.email, 'preferences': request.form.getlist('food'), 'time_pref': timeDiff })

        value = form_groups(mongo.db.being_matched, mongo.db.groups)
        print(value)
        if(value):
            # Return to bryan's page
            return "You were matched"
            pass
        else:
            return redirect(url_for('matching', time_pref=round(timeDiff)))


    time = datetime.datetime.utcfromtimestamp(current_user.time_pref)
    time_string = time.strftime("%I:%M %p")
    time_string2 = "'" + time_string + "'"
    print("time_string", time_string)
    print("time_string2", time_string2)
    return render_template('preferences.html', preference_list=current_user.food_prefs, time_pref=time_string2)


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


@app.route("/matching")
def matching():
    print('current_user.time_pref:', current_user.time_pref)
    print('time_pref:', request.args['time_pref'])
    # produce datetime obj from seconds-since-epoch time_pref on current_user (add subtract 30 minutes to get notification time)
    dateFormatted = datetime.datetime.utcfromtimestamp(float(request.args['time_pref']) - 1800.0)

    # send current_user's email and formatted time to matching.html
    return render_template("matching.html", time=(dateFormatted.strftime('%I:%M %p')))


if __name__ == "__main__":
    socketio.run(app, debug=True)  # debug = true to put in debug mod
