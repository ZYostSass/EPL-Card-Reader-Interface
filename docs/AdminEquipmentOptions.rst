Admin Equipment Options Guide
=============================

Manage
-------

Will display a list of all current machines in the database including their ID and name.
The machine database is dynamic and machine functionality is driven by the database.

The Machine Class 
-------------------
.. autoclass:: database.class_models.Machine

Adding a Machine
-----------------

.. autofunction:: database.user_options.add_machine

Removing a Machine
-------------------
ID is automatically incremented whenever a machine is added. If a machine is deleted, the
list will not contract but will have a gap; but the ID # for each machine will persist.

.. autofunction:: database.user_options.remove_machine

Note that the actual template manage_equipment.html removes the selected machine like so:

>>> ('views.remove_equipment', name=row.name)

Editing Machine Names 
----------------------

Also allows for editing machine names, as labs at PSU are known for their whimsical nicknames:

.. autofunction:: database.user_options.edit_machine

Once again, the manage_equipment template form takes care of this for us.
