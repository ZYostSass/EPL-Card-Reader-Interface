import user_options

print("\n")
# Check in base admin - sure hit
print("Checking in user with ID: 0 (Base Admin)")
given_user = user_options.checkin_user(0)
print("Welcome", given_user)
print("\n")

# Display the name and ID of base admin
print("Display the name and ID of user with ID: 0 (Base Admin)")
given_user = user_options.get_user_data(0)
if given_user != None:
    print("First Name:", given_user[0], "\nLast Name:", given_user[1], "\nID Number: ", given_user[2])
else:
    print("User does not exist")
print("\n")

# Check in unregistered user - sure miss
print("Checking is user with ID: 2345 (Doesn't Exist)")
given_user = user_options.get_user_data(2345)
if given_user != None:
    print("First Name:", given_user[0], "\nLast Name:", given_user[1], "\nID Number: ", given_user[2])
else:
    print("User does not exist")
print("\n")

# Output list of all users in database
print("Outputting all users in the table")
output_list = user_options.read_all()
for n in range(len(output_list)):
    print(output_list[n])
print("\n")

# Duplicate user check
print("Adding duplicate Base Admin: John Doe")
user_options.add_new_user(0, 0, "John", "Doe", "jdoe@pdx.edu", "Admin", user_options.class_models.datetime.datetime.now())
print("\n")

# New User Addition
print("Adding new user: Jane Jackson")
user_options.add_new_user(1, 1, "Jane", "Jackson", "jjack@pdx.edu", "Student", user_options.class_models.datetime.datetime.now())
output_list = user_options.read_all()
for n in range(len(output_list)):
    print(output_list[n])
print("\n")

# Change a given User's role
print("Changing new user to Manager")
user_options.change_user_access_level(1, "Manager")
output_list = user_options.read_all()
for n in range(len(output_list)):
    print(output_list[n])
print("\n")

# Remove added user
print("Removing new user: Jane Jackson")
user_options.remove_user(1)
output_list = user_options.read_all()
for n in range(len(output_list)):
    print(output_list[n])
print("\n")

# Add trainings to existing user
print("Adding OSH Park training to Base Admin")
user_options.add_training(0, 0)
to_display = user_options.checkin_user(0)
print(to_display, "\n")
for n in range(len(to_display.machines)):
    print(">", to_display.machines[n], "\n")
print("\n")

# Remove trainings to existing user
print("Removing OSH Park training to Base Admin")
user_options.remove_training(0, 0)
to_display = user_options.checkin_user(0)
print(to_display, "\n")
for n in range(len(to_display.machines)):
    print(">", to_display.machines[n], "\n")
print("\n")

# Output list of all machines and their trained users
print("Outputting all machines and trained users")
output_list = user_options.read_all_machines()
for n in range(len(output_list)):
    print(output_list[n])
print("\n")

# Add new machine to the database
print("Adding new machine 'New_One' to the table")
user_options.add_machine("New_One")
output_list = user_options.read_all_machines()
for n in range(len(output_list)):
    print(output_list[n])
    for m in range(len(output_list[n].trained_users)):
        print(" >", output_list.trained_users[m])
print("\n")

# Remove non-existant machine from the database
print("Remove non-existant machine 'Old_One' from the table")
user_options.remove_machine("Old_One")
print("\n")

# Remove new machine from the database
print("Remove  machine 'New_One' from the table")
user_options.remove_machine("New_One")
output_list = user_options.read_all_machines()
for n in range(len(output_list)):
    print(output_list[n])
    for m in range(len(output_list[n].trained_users)):
        print(" >", output_list.trained_users[m])