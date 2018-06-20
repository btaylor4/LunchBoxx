from group import Group


def form_groups(users_collection, being_matched_collection, group_collection):
    usersCursor = being_matched_collection.find()
    print('BS')
    users = list(usersCursor)
    print('Users', users)
    if(len(users) < 5):
        return None
    for index in range(0, len(users), 5):
        grouped_users = (users[index:index+5])
        group_emails = []
        for user in grouped_users:
            group_emails.append(user['email'])
        group = Group(group_emails)
        # TODO get time
        # TODO Get restaurant
        group_collection.insert({'emails': group_emails})
        print(group_emails)
        stats = being_matched_collection.remove({'email':{'$in':group_emails}})
        users_collection.update({'email':{'$in':group_emails}}, {'$set': {'status': "matched"}})
        # TODO sets user status
        print(stats)
        return group