Dashboard Overview
===================

Dashboard - Home
------------------
The dashboard comes with a home page for admins to manipulate students and equipment, as well as view recent scan-ins.

Equipment Overview
-------------------
Displays all the current machines for the lab. Machines are broken up by their category.
As of the current iteration, clicking on their icons will take you to the EPL's webpage on that machine.

Refer to `Admin Equipment Options <AdminEquipmentOptions.html>`__

Permissions
------------
Takes a user's badge # and returns all machines in the lab, with approved machines outlined in green
and untrained machines outlined in red.

.. autofunction:: database.user_options.get_user

Waiver
-------
PSU's EPL Safety Waiver is embedded directly within the app using the following html iframe method:
Refer to the 'waiver.html' template under web_app/templates.

>>><iframe class="responsive-iframe shadow" 
                   src="https://docs.google.com/forms/d/e/1FAIpQLSfxIUOoJnwgw2woPsUDmwpgH4uHPu-xNtaJN9nRBLdbHWztlA/viewform"
    
    iframe>

