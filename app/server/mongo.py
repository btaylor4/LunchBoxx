import sys
from pymongo import MongoClient

client = MongoClient(
    'mongodb://slackers:bigwilli3@ds263460.mlab.com:63460/lunchbox')

if __name__ == "__main__":
    if sys.argv[1] == 'purge':
        client.lunchbox.users.delete_many({})
        print('Data base has been purged!')
