Admin Usage Guide
====
.. _Dashboard

Dashboard
----------

The dashboard consists of several core functionalities inlcuding student, equipment and training management:

.._Student

The 'add student' button will take you to the add-user-form html page.

The `user_options.add_new_user(psu_id, access, firstname, lastname, email, role)` function
will take all of these values from the web page prompts. It will check if the PSU ID is already present.
`to_check` uses a helper function to check the database for the unique PSU ID number.



