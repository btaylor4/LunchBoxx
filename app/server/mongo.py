import sys
from pymongo import MongoClient

client = MongoClient(
    'mongodb://slackers:bigwilli3@ds263460.mlab.com:63460/lunchbox')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'purge':
        if len(sys.argv) > 2 and sys.argv[2] == 'users':
            client.lunchbox.users.delete_many({})
            print('User data base has been purged!')

        if len(sys.argv) > 2 and sys.argv[2] == 'groups':
            client.lunchbox.groups.delete_many({})
            print('Groups data base has been purged!')

        if len(sys.argv) > 2 and sys.argv[2] == 'being_matched':
            client.lunchbox.being_matched.delete_many({})
            print('Being matched data base has been purged!')

        if len(sys.argv) > 2 and sys.argv[2] == 'all':
            client.lunchbox.users.delete_many({})
            client.lunchbox.groups.delete_many({})
            client.lunchbox.being_matched.delete_many({})
            print('All data bases have been purged!')

    print('Missing data base paramater')
