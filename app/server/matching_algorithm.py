from group import Group
from geopy import distance

MATCH_RANGE = 5 # miles
FRIEND_COUNT = 5

# recursively find friends
def findFriends(user, pool, friends, accepted_foods, count):
    # base case
    if(count==0):
        return friends

    # find match
    friend = findMatch(user, pool, accepted_foods)

    if(friend==None):
        return []

    # add friend to friend list
    pool.remove(friend)
    friends.append(friend)

    # get next friend
    print(count)
    count = count-1
    friends += findFriends(friend, pool, friends, accepted_foods, count)
    return friends



# find a match
def findMatch(user, pool, accepted_foods):
    # for the user, get all users that match the user the most
    for other_user in pool:    

        print(user['email'] + ' is searching if ' + other_user['email'] + ' is compatible')

        # if the user has the same time
        if(user['time_pref'] == other_user['time_pref']):
        
            print(user['email'] + ' has the same time preferenc')
            
            # make sure addresses are in 5 mile range
            if(distance.distance((user['lat'], user['long']), (other_user['lat'], other_user['long'])).miles < MATCH_RANGE):
        
                print(user['email'] + ' found someone in distance range')
                print('here are your accepted foods: ' + ', '.join(accepted_foods))
                print('here the others accepted foods: ' + ', '.join(other_user['food_prefs']))
                # make sure the people like the same food
                common_foods = list(
                    set(accepted_foods).intersection(other_user['food_prefs']))
                print('here are the common foods: ' + ', '.join(common_foods))

                # move on if common foods were found
                if(len(common_foods) > 0):
    
                    print(user['email'] + ' found someone common foods')
                    
                    common_interests = list(set(user['interest_prefs']).intersection(other_user['interest_prefs']))

                    if(len(common_interests) > 0):
                        
                        print(user['email'] + ' found someone with common interests')
                        
                        # accept the common foods
                        accepted_foods = common_foods
                        
                        # return the other user as a friend
                        return other_user


# form groups
def form_groups(users_collection, being_matched_collection, group_collection):
    usersCursor = being_matched_collection.find()
    print('BS')
    pool = list(usersCursor)
    print('Users', pool)

    # create the list of formed groups to be returned
    formed_groups = []

    while(len(pool) >= FRIEND_COUNT):
        # create lists to fill out
        chosen_user = pool.pop()

        print('chosen user: ')
        for element in chosen_user:
            print(element)
    
        accepted_foods = chosen_user['food_prefs']
        friends = findFriends(
            chosen_user, pool, [chosen_user], accepted_foods, FRIEND_COUNT)
        friends.append(chosen_user)

        if(friends != None):

            # re-add the users back to the pool if there weren't enough matched
            if(len(friends) <= FRIEND_COUNT):
                pool += friends.remove(chosen_user)
            else:
                # generate the groups emails
                group_emails = []
                for user in friends:
                    group_emails.append(user['email'])

                # create a new group
                group = Group(group_emails)
                formed_groups.append(group)

                # fix databases
                print(group_emails)
                group_collection.insert({'emails': group_emails}) # TODO: grab restaurant time preference
                stats = being_matched_collection.remove({'email': {'$in': group_emails}})
                print(stats)
                users_collection.update({'email': {'$in': group_emails}}, {'$set': {'status': "matched"}})                                

    return formed_groups
        

    '''
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
    '''
