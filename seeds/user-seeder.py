from flask_seeder import Seeder, Faker, generator

import sys
import os
# sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web_app')))
from web_app.models import User

class UserSeeder(Seeder):

  def run(self):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
      cls=User,
      init={
        "id": generator.Integer(),
        "fname": generator.Name(),
        "lname": generator.Name(),
        "email": generator.Email(),
        "badge": generator.String("[a-z]{20}"),
        "manager": True,
        "admin": True,
      }
    )

    # Create 5 users
    for user in faker.create(5):
      print("Adding user: %s" % user)
      self.db.session.add(user)
