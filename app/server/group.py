import random


class Group(object):
    def __init__(self, emails):
        self.emails = emails
        self.time = 0
        self.restaurant = ''

    def get_id(self):
        return self.group_id
