from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, User, Activity, Occurrence, connect_to_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "7SOIF280FSH9G0-SSKJ"


@app.route("/")
def show_landing_page():
    """Return landing page."""

    return render_template("landing.html")


@app.route("/signup", methods=["GET"])
def display_signup_form():
    """Return form for signing up for an account."""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_user():
    """Process signup form, adding user to database."""

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    age = request.form.get("age")

    # Check database for pre-existing account by checking for a user with the
    # provided email address
    if User.query.filter(User.email == email).all():
        flash("Looks like you've already registered. If you mistyped, please tr\
               y again.")

        return redirect("/signup")

    else:
        if age:
            new_user = User(user_handle=username,
                            password=password,
                            email=email,
                            age=age)

        else:
            new_user = User(user_handle=username,
                            password=password,
                            email=email)

        db.session.add(new_user)
        db.session.commit()

    return redirect("/setup")


@app.route("/setup", methods=["GET"])
def request_activity_types():
    """Display form for user to choose the activities they want to track."""

    return render_template("setup.html")


@app.route("/setup", methods=["POST"])
def create_activity_types():
    """Process setup form, adding user-defined activity types to database."""

    # TODO test user can add an activity :D Look up integration test.

    # Make sure user is logged in
    if session.get("user_id", 0) == 0:
        flash("You need to be logged in to view this page. Please log in.")
        return redirect("/signin")

    activity_1 = request.form.get("activity_1")
    activity_2 = request.form.get("activity_2")
    activity_3 = request.form.get("activity_3")
    activity_4 = request.form.get("activity_4")
    activity_5 = request.form.get("activity_5")
    activity_6 = request.form.get("activity_6")
    activity_7 = request.form.get("activity_7")
    activity_8 = request.form.get("activity_8")
    activity_9 = request.form.get("activity_9")
    activity_10 = request.form.get("activity_10")

    activities = [activity_1, activity_2, activity_3, activity_4, activity_5,
                  activity_6, activity_7, activity_8, activity_9, activity_10]

    new_activities = []

    for activity in activities:
        if activity:
            new_activities.append(activity)

    # Handle submission of form with no values
    if new_activities == []:

        flash("""You need to enter at least one activity to contine.
              Please make a selection and try again.""")
        return redirect("/setup")

    # For every activity user provides, add activity to the database
    else:

        for activity in new_activities:
            new_activity = Activity(activity_type=activity,
                                    user_id=session["user_id"])

            db.session.add(new_activity)
        db.session.commit()

        flash("Great! Looks like you're ready to start tracking!")
        return redirect("/main")


@app.route("/signin", methods=["GET"])
def display_signin_form():
    """Display form for logging into existing account."""

    return render_template("signin.html")


@app.route("/signin", methods=["POST"])
def signin_user():
    """Handle sign-in."""

    password = request.form.get("password")
    email = request.form.get("email")

    # Check that a user with the provided email address is already in database
    if User.query.filter(User.email == email).all():
        # If so, check that in the database, the password for the user with the
        # provided email address matches the password provided
        if User.query.filter(User.email == email).one().password == password:
            # If so, get the user's user_id and store it on the session
            user_id = User.query.filter(User.email == email).one().user_id
            session["user_id"] = user_id

            flash("Thanks for logging in!")
            return redirect("/main")

    else:
        flash("Sorry, we didn't find an account with the email and password you\
               provided. Please try again.")
        return redirect("/signin")


@app.route("/main", methods=["GET"])
def show_main_page():
    """Load main page."""

    # Get activities for dropdown menu for choosing one to plan
    activities = Activity.query.filter(Activity.user_id == session['user_id']).all()

    # Get list of user's occurrences without end times & before ratings
    user = User.query.filter(User.user_id == session['user_id']).first()
    planned_occurrences = user.get_planned_occurrences()

    return render_template("/main.html",
                           activities=activities,
                           planned_occurrences=planned_occurrences)


@app.route("/plan_activity", methods=["POST"])
def handle_activity_choice():
    """Handle form for planning an activity."""

    activity_id = request.form.get("activity-choice")

    return redirect("/record_before/" + activity_id)


@app.route("/record_before/<activity_id>", methods=["GET"])
def display_before_form(activity_id):
    """Display form for creating a new occurrence."""

    return render_template("/record_before.html", activity_id=activity_id)


@app.route("/record_before/<activity_id>", methods=["POST"])
def get_before_values(activity_id):
    """Process form, creating a new occurrence and saving it to the database."""

    before_rating = request.form.get("before-rating")
    now_start = request.form.get("now-start")
    start_hour = request.form.get("planned-time")
    start_date = request.form.get("planned-date")

    if now_start:
        start_time = datetime.now()
    else:
        unformatted_time = start_date + " " + start_hour
        print unformatted_time
        start_time = datetime.strptime(unformatted_time, "%m/%d/%Y %I:%M %p")

    new_occurrence = Occurrence(activity_id=activity_id,
                                start_time=start_time,
                                before_rating=before_rating)

    db.session.add(new_occurrence)
    db.session.commit()

    flash("Entries successfully saved.")
    return redirect("/main")

# @app.route("/record_after/<activity_id>", methods=["GET"])
# def display_after_form(activity_id):

#     # CODE

# @app.route("/record_after/<activity_id>", methods=["POST"])
# def get_after_values(activity_id):

#     after_rating = request.form.get("after_rating")
#     end_time = request.form.get("end_time")



# For additional routes, a stub:

# @app.route("/main")
# def ______():
#     """ DOCSTRING"""

#   CODE

#    return CODE

connect_to_db(app)

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
