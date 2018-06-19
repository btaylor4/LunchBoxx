from group import Group


def form_groups(user_collection, group_collection):
    users = user_collection.find()
    if(len(users) < 5):
    	return None
	for index in range(0, len(users), 5):
		group_emails = (users[index:index+5])
		group = Group(group_emails)
		group.time = users
		# TODO get time
		# TODO Get restaurant
		group_collection.insert(group)
		return group
