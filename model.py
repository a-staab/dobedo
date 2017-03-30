from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User. A user has many activities."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(50), nullable=False, unique=True)
    password = db.Column(db.Unicode(25), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    user_handle = db.Column(db.Unicode(50), nullable=False)

    def __repr__(self):
        return "<User with user_id %s and email %s>" % (self.user_id,
                                                        self.email)


class Activity(db.Model):
    """Activity. An activity has many occurrences."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_type = db.Column(db.Unicode(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    user = db.relationship("User", backref="activities")

    def __repr__(self):
        return "<Activity with activity_id %s by user_id %s>" % (
            self.activity_id, self.user_id)


class Occurrence(db.Model):
    """Occurrence. An occurrence has one activity. An occurrence has one user."""

    __tablename__ = "occurrences"

    occurrence_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    before_rating = db.Column(db.Integer, nullable=False)
    after_rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Unicode(350), nullable=True)

    activity = db.relationship("Activity", backref="occurrences")

    def __repr__(self):
        return "<Occurrence with occurrence_id %s and activity_id %s>" % (
            self.occurrence_id, self.activity_id)

# TODO: def add_new_user():


def connect_to_db(app):
    """Connect to the database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///tracker'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB! Woo!"
