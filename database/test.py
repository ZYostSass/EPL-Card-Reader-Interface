import user_options

print("\n")
# Check in base admin - sure hit
print("Checking is user with ID: 0 (Base Admin)")
given_user = user_options.checkin_user(0)
print("Welcome", given_user)
given_user = user_options.get_user_data(0)
print("First Name:", given_user[0], "\nLast Name:", given_user[1], "\nID Number: ", given_user[2])
print("\n")

# Check in unregistered user - sure miss
print("Checking is user with ID: 2345 (Doesn't Exist)")
user_options.checkin_user(2345)
print("\n")

# Output list of all users in database
print("Outputting all users in the table")
user_options.read_all()
print("\n")

# Duplicate user check
print("Adding duplicate Base Admin: John Doe")
user_options.add_new_user(0, 0, "John", "Doe", "jdoe@pdx.edu", "Admin")
print("\n")

# New User Addition
print("Adding new user: Jane Jackson")
user_options.add_new_user(1, 1, "Jane", "Jackson", "jjack@pdx.edu", "Student")
user_options.read_all()
print("\n")

# Remove added user
print("Removing new user: Jane Jackson")
user_options.remove_user(1)
user_options.read_all()
print("\n")

# Add trainings to existing user
print("Adding OSH Park training to Base Admin")
user_options.add_training(0, 0)
print("\n")

# Remove trainings to existing user
print("Revmoving OSH Park training to Base Admin")
#user_options.remove_training(0, 0)
print("\n")

# Output list of all machines and their trained users
print("Outputting all machines and trained users")
user_options.read_all_machines()
print("\n")

# Add new machine to the database
print("Adding new machine 'New_One' to the table")
user_options.add_machine("New_One")
user_options.read_all_machines()
print("\n")

# Remove non-existant machine from the database
print("Remove non-existant machine 'Old_One' from the table")
user_options.remove_machine("Old_One")
print("\n")

# Remove non-existant machine from the database
print("Remove  machine 'New_One' from the table")
user_options.remove_machine("New_One")
user_options.read_all_machines()
print("\n")

#user_options.user_check("John", "Doe")
#user_options.change_user_training(1,1,1)
# user_options.chance_user_access_level()
#user_options.change_user_access_level(1, "Manager")
user_options.read_all()
