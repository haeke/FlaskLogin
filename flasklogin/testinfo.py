import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import *

engine = create_engine('sqlite:///users.db', echo=True)

#create a session
Session = sessionmaker(bind=engine)
session = Session()

user = User("edwin", "password")
session.add(user)

user = User("test", "anothertest")
session.add(user)

user = User("mongo", "database")
session.add(user)

#commit the record to the database
session.commit()

session.commit()
session.commit()
