"""Utility file to seed tracker database from data in seed_data/"""

from model import User, Activity, Occurrence, connect_to_db, db
from server import app

def load_users():
    """Load users from u.user into database."""

    print "Users"

def load_activities():
    """Load activities from u.activity into database."""

    print "Activities"

def load_occurrences():
    """Load occurrences from u.occurrence into database."""

    print "Occurrences"

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_activities()
    load_occurrences()
    set_val_user_id()