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
from datetime import datetime
from time import time
from datetime import timedelta, datetime
from places import getLatLong

import json
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


def getInterests():
    with open('interests.json') as f:
        data = json.load(f)
        return data['interests']


def getFoods():
    with open('foods.json') as f:
        data = json.load(f)
        return data['foods']


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

            print('daddy data: ', getInterests())

            if requested_user is None:
                if password == verify_password:
                    if(len(password) > 5):
                        # makes a new user inside data base if non already exits
                        return render_template('create-profile.html', email=email, password=hashed_password, hidden='hidden', interests=getInterests(), foods=getFoods())
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

            now = datetime.utcnow()

            print('now:', now)

            tempTimeString = now.strftime("%d%m%Y") + " " + form['lunch-time']

            print('tempTimeString:', tempTimeString)

            tempTime = datetime.strptime(
                tempTimeString, "%d%m%Y %I:%M %p")

            print('tempTime:', tempTime)

            time_diff_datetime = (tempTime-datetime(1970, 1, 1))
            timeDiff = time_diff_datetime.total_seconds()
            # If within an hour, sign them up for lunch the next day
            present = datetime.now()

            print('Timediff float', timeDiff)
            print('Timediff int', int(timeDiff))
            if present > (datetime.utcfromtimestamp(timeDiff) - timedelta(hours=1)):
                timeDiff = timeDiff + 86400
                print('New timediff', timeDiff)

            timeDiff = time_diff_datetime.total_seconds()

            print('timeDiff:', timeDiff)

            user.first_name = form['firstName']
            user.last_name = form['lastName']
            user.time_pref = round(timeDiff)
            user.addr = form['address']

            # handle errors
            if(user.first_name == ''):
                return render_template('create-profile.html', email=email, password=password, error='First name can not be empty.', interests=getInterests(), foods=getFoods())
            elif(user.last_name == ''):
                return render_template('create-profile.html', email=email, password=password, error='Last name can not be empty.', interests=getInterests(), foods=getFoods())
            # TODO: see if address exits (google maps)
            elif(user.addr == '' or not getLatLong(user.addr)):
                return render_template('create-profile.html', email=email, password=password, error='Address is invalid.', interests=getInterests(), foods=getFoods())

            # preferences
            if('interests' in form):
                user.interest_prefs = form.getlist('interests')
            if('food' in form):
                user.food_prefs = form.getlist('food')

            lat, long = getLatLong(user.addr)
            update = {'email': form['email'], 'password': form['password'], 'first_name': user.first_name, 'last_name': user.last_name, 'time_pref': user.time_pref, 'addr': user.addr,
                      'interest_prefs': user.interest_prefs, 'food_prefs': user.food_prefs, 'lat': lat, 'long': long, 'status': "not_matched"}

            # find and update user
            mongo.db.users.insert(update)

            # redirect to the login page
            return redirect(url_for('login'))
        elif(request.form['nextButton'] == 'back'):
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
                login_user(user, force=True)
                return redirect(url_for('user_portal'))
        return render_template('login.html', error='Incorrect username or password.')

    return render_template('login.html', hidden='hidden')


@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':

        now = datetime.utcnow()
        tempTimeString = now.strftime(
            "%d%m%Y") + " " + request.form['lunch-time']
        tempTime = datetime.strptime(tempTimeString, "%d%m%Y %I:%M %p")
        timeDiff = (tempTime-datetime(1970, 1, 1)).total_seconds()

        mongo.db.being_matched.insert({'email': current_user.email, 'first_name': current_user.first_name, 'last_name': current_user.last_name,
                                       'addr': current_user.addr, 'interest_prefs': current_user.interest_prefs, 'food_prefs': request.form.getlist('food'), 'time_pref': timeDiff, 'lat': current_user.lat, 'long': current_user.long})
        mongo.db.users.update({'email': current_user.email}, {
                              '$set': {'status': "being_matched"}})
        value = form_groups(
            mongo.db.users, mongo.db.being_matched, mongo.db.groups)
        print(value)
        if(value):
            # Return to bryan's page
            return "You were matched"
            pass
        else:
            return redirect(url_for('matching', time_pref=round(timeDiff)))

    time = datetime.utcfromtimestamp(current_user.time_pref)
    time_string = time.strftime("%I:%M %p")
    time_string2 = "'" + time_string + "'"
    print("time_string", time_string)
    print("time_string2", time_string2)
    return render_template('preferences.html', preference_list=current_user.food_prefs, time_pref=time_string2, foods=getFoods())


@app.route('/places', methods=['GET', 'POST'])
def place():
    print("I AM IN PLACE YO")
    # food_type = 'italian'
    # coord = (26.0895906,-80.3669549)
    # resp = places.getNearbyPlaces(food_type, coord)
    # print("The top restaurant is: ", resp)

    location = 'I AM NOT REAL YO'
    resp = places.getLatLong(location)
    print("The lat and long is:", resp)
    return


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/")
def index():  # TODO: Check if user is logged in
    return redirect(url_for("login"))


@app.route("/user-portal")
@login_required
def user_portal():

	user_group = {}

	if (current_user.status == 'matched'):
		all_groups = mongo.db.groups.find({});
		all_groups = list(all_groups)

		for group in all_groups:
			if current_user.email in group['emails']:
				user_group["emails"] = group['emails']
				user_group["restaurant"] = group['restaurant']
				user_group["time"] = group["time"]

				time = datetime.utcfromtimestamp(user_group["time"])
				user_group["time"] = time.strftime("%I:%M %p")

	print("The other user's emails are: ", user_group["emails"])

	profiles = []
	for email in user_group["emails"]:
		profiles.append(mongo.db.users.find_one({"email": email}))

	user_group["emails"] = profiles

	print(user_group)

	return render_template("user-portal.html", status=current_user.status, user=getUserDict(), user_group=user_group)


def getUserDict():
    u = {}
    for attr, value in current_user.__dict__.items():
        propertyName = attr.replace("_", " ").title()
        property = value

        if isinstance(value, list):
            property = " ".join(value)
        u[propertyName] = property

    del u['Password']
    del u['Status']

    time = datetime.utcfromtimestamp(u['Time Pref'])
    u['Time Pref'] = time.strftime("%I:%M %p")

    return u


@app.route("/matching")
def matching():
    print('current_user.time_pref:', current_user.time_pref)
    print('time_pref:', request.args['time_pref'])
    # produce datetime obj from seconds-since-epoch time_pref on current_user (add subtract 30 minutes to get notification time)
    dateFormatted = datetime.utcfromtimestamp(
        float(request.args['time_pref']) - 1800.0)

    # send current_user's email and formatted time to matching.html
    return render_template("matching.html", time=(dateFormatted.strftime('%I:%M %p')))


if __name__ == "__main__":
    socketio.run(app, debug=True)  # debug = true to put in debug mod
