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
        self.lat = 0.0
        self.long = 0.0
        self.status = 'not matched'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def db_user(self, db_user):
        self.addr = db_user['addr']
        self.email = db_user['email']
        self.first_name = db_user['first_name']
        self.last_name = db_user['last_name']
        self.interest_prefs = db_user['interest_prefs']
        self.food_prefs = db_user['food_prefs']
        self.time_pref = db_user['time_pref']
        self.lat = db_user['lat']
        self.long = db_user['long']
        self.status = db_user['status']
        return self
