
class BeingMatched(object):
    def __init__(self, email):
        self.email = email
        self.preferences = []
        self.time = 0

    def get_id(self):
        return self.email
