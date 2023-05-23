Admin Student Options Guide
============================
.. _Dashboard:

Dashboard
----------

The dashboard consists of several core functionalities inlcuding student, equipment and training management:

Add Student
-----------------------------

The 'add student' button will take you to the add-user-form html page.

.. autofunction:: database.user_options.add_new_user

Will take all of these values from the web page prompts. It will check if the PSU ID is already present.
`to_check` uses a helper function to check the database for the unique PSU ID number.

.. autofunction:: database.user_options.is_user_id_present

If the psuID is duplicated, we throw a value error as PSUIDs should be unique.
The html page itself comes with preemptive error checking and should catch incorrect types.
Such as non-ints for access badge numberss, or non-pdx.edu emails.

Edit Student
-------------

The 'edit' button will take you to the edit_user html page. 

'Remove Student' allows for the removal of a student from the database.

.. autofunction:: database.user_options.remove_user

Promote User
-------------

The 'promote' button takes you to the /promote html page.

'Promote Student' will allow the user to promote an existing student to manager or admin.
As a reminder, the key difference is that admins have the power to promote other students/managers.

.. autofunction:: database.user_options.change_user_access_level

Using WTForms, this page has a bubble-select option for Admin or Manager. It will enforce a password
setting option for admins and managers, as they will have more access to the app and user info.

With information accurately set, calls promote from user class:

.. autofunction:: database.class_models.User.promote

Edit User
----------

WIP. Functionality working.