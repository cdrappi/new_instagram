import os, sys
import configs
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

# association_table = Table('association', Base.metadata,
#     Column('profile_id', Integer, ForeignKey('profile.user_id')),
#     Column('profile_id', Integer, ForeignKey('profile.user_id')),
# )

class Profile(Base):
    __tablename__ = 'profile'

    user_id   = Column(Integer, primary_key=True) # a user's ID as assigned by Instagram

    username  = Column(String(250), unique=True, nullable=False) # note: a user can change their username,
    link      = Column(String(300), unique=True, nullable=False) # which can create collisions

    name        = Column(String(250), nullable=True)
    description = Column(String(10000), nullable=True)
    website     = Column(String(1000), nullable=True)


    degree        = Column(Integer, nullable=False) # how far away this person is from seed users   
    num_posts     = Column(Integer, nullable=False)
    num_follows   = Column(Integer, nullable=False)
    num_followers = Column(Integer, nullable=False)

    # followers = relationship("Profile", secondary=association_table)

    def __repr__(self):
        return self.username


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(configs.DB_NAME)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)


