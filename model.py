from flask_sqlachemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User. A user has many activities."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, nullable=True)           # optional, permits aggregate analysis
    user_handle = db.Column(db.String(50), nullable=True)  # nice for anonymity, but no sharing planned (yet?)}

    def __repr__(self):
     # TODO change email here to user_handle if implementing (and nullable to False)
        return "<User with user_id %s and email %s>" % (self.user_id,
                                                        self.email)


class Activity(db.Model):
    """Activity. An activity has many occurences."""

    __tablename__ = "activities"

    act_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    act_type = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    is_active = db.Column(db.Boolean, nullable=False)

    user = db.relationship("User", backref="activities")

    def __repr__(self):
        return "<Activity with act_id %s by user_id %s>" % (self.act_id,
                                                            self.user_id)


class Occurence(db.Model):
    """Occurence. An occurence has one activity. An occurence has one user."""

    __tablename__ = "occurences"

    occurrence_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    act_id = db.Column(db.Integer, db.ForeignKey('activities.act_id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    before_rating = db.Column(db.Integer, nullable=False)
    after_rating = db.Column(db.Integer, nullable=False)
    notes_about = db.Column(db.String(350), nullable=True)

    activity = db.relationship("Activity", backref="occurences")


    def __repr__(self):
        return "<Occurence with occurence_id %s and act_id %s>" % (
            self.occurence_id, self.act_id)
