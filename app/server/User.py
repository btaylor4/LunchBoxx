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
