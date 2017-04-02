from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User. A user has many activities."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(50), nullable=False, unique=True)
    password = db.Column(db.Unicode(25), nullable=False)
    user_handle = db.Column(db.Unicode(50), nullable=False)
    age = db.Column(db.Integer, nullable=True)

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

def connect_to_db(app):
    """Connect to the database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///tracker'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

# Helper functions


def create_new_user(email, password, user_handle, age=None):

    return User(email=email,
                password=password,
                user_handle=user_handle,
                age=age)

    # v--Should this be included? Removed so I could use function inside
    #    example_data() below
    # db.session.add(new_user)
    # db.session.commit()


def example_data():
    """Sample data for testing."""

    # Test creation of new users

    # Test using instantiation
    ashley = User(email='hb-student@hackbright.com', password='python',
                  user_handle='artist')

    # Question: since create_new_user includes session commit, will running the
    # two following lines of code create soo and hannah twice?

    # Tests using create_new_user helper function
    soo = create_new_user('coding-student@hackbright.com', 'python', 'boss')
    hannah = create_new_user('hacks@hackbright.com', 'python', 'linguist')

    # Test supplying an age, which is optional
    mel = User(email='mel@ubermelon.com',
               password='python',
               user_handle='melons_honcho',
               age=42)

    # ______ Move to these two to tests.py because they require session? _______
    # # Test activity setup, which requires session data
    # active_activity = Activity(activity_type='coding',
    #                            user_id=session["user_id"])

    # # Test is_active can be specified too (though this change wouldn't normally
    # # be set at creation time)
    # inactive_activity = Activity(activity_type='coding',
    #                              user_id=session["user_id"],
    #                              is_active=False)
    # _________________________________________________________________________

    # Test that an occurrence can be created without end_time, after_rating, and
    # notes
    # t_occurrence_1 = Occurrence(activity_id=1, start_time=, before_rating=,

    # Test that an occurrence can be created with values for all attributes

    # t_occurence_2 = Occurrence(activity_id=2, start_time=, end_time=,
    # before_rating=, after_rating=, notes=)

    # Test than an occurrence can be updated

    # t_occurence_1 = (set values for end_time, after_rating, and notes)

    # ^--Once complete, add test occurrences to list--v
    db.session.add_all([ashley, soo, hannah, mel])
    db.session.commit()

if __name__ == "__main__":
    from server import app, session
    connect_to_db(app)
    print "Connected to DB! Woo!"
