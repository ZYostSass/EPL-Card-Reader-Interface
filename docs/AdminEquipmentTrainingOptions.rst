Training Guide
================

This program uses the Flask framework and, through that, SQLAlchemy for its database schema.

`Flask SQLAlchemy's Webpage and Guide <https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/>`_

The training sessions take advantage of a many-to-many relationship between students and machines. 
Using the relationship syntax:

>>> In User:
>>>     machines: Mapped[Optional[list["Machine"]]] = relationship(secondary = user_machine_join_table, back_populates="trained_users")
>>> In Machine:
>>>     trained_users: Mapped[Optional[list["User"]]] = relationship(secondary = user_machine_join_table, back_populates="machines")

Creates a table that ties together a given user to a list of machines. This is done using: 

.. autofunction:: database.user_options.add_training