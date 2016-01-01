import helpers, dirs, configs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Profile

def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True

 
engine = create_engine(configs.DB_NAME)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 

influencers, infl_header = helpers.load_csv(dirs.dirs_dict["discoveries"]["instagram"])

# Insert a Profile in the profile table
for influencer in influencers:
    for key in ('time_pulled', ):
        influencer.pop(key)
    profile = Profile(**influencer)
    profile_record, created = get_or_create(session, Profile, defaults=influencer, user_id=influencer['user_id'])
    print('created' if created else '--existed')









