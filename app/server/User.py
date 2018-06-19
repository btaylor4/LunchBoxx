class User(object):
    def __init__(self, email, password, first_name, last_name, interest_prefs, food_prefs, time_pref, addr):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.interest_prefs = interest_prefs
        self.food_prefs = food_prefs
        self.time_pref = time_pref
        self.addr = addr
