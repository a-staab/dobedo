from flask_sqlachemy import SQLAlchemy

db = SQLAlchemy

# Open question: To denormalize or not to denormalize? Does the user_id belong
# in both the Activity and Occurence tables?


class User(db.Model):
    """   DOCSTRING  """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, nullable=True)           # optional, permits aggregate analysis
    user_handle = db.Column(db.String(50), nullable=True)  # nice for anonymity, but no sharing planned (yet?)}

    def __repr__(self):
        return "< ... >"


class Activity(db.Model):
    """   DOCSTRING  """

    __tablename__ = "activities"

    act_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    act_type = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    is_active = db.Column(db.Boolean, nullable=False)

#TODO

#Create relationship

    def __repr__(self):
        return "< ... >"


class Occurence(db.Model):
    """   DOCSTRING """

    __tablename__ = "occurences"

    occurrence_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    act_id = db.Column(db.Integer, db.ForeignKey('activities.act_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # <--Do we want this here?
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    before_rating = db.Column(db.Integer, nullable=False)
    after_rating = db.Column(db.Integer, nullable=False)
    notes_about = db.Column(db.String(350), nullable=True)

    def __repr__(self):
        return "< ... >"

#TODO

#Create relationships
