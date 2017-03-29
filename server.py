from flask import Flask, request, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret.key = "7SOIF280FSH9G0-SSKJ"


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

    # Get fields data from request object

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    age = request.form.get("age")

    # Check database for pre-existing account by checking for email

    if User.query.filter(User.email == email).all():
        # TODO - Improve UX here?
        flash("Looks like you've already registered. If you mistyped, please try again.")
        
    else:
        new_user = User(username=username,
                        password=password,
                        email=email
                        age=age)

        db.session.add(new_user)
        db.session.commit()

    return  # CODE


@app.route("/setup", methods=["GET"])
def request_act_types():
    """Display form for user to choose the activities they want to track."""

    return render_template("setup.html")


@app.route("/setup", methods=["POST"])
def create_act_types():
    """Process setup form, adding user-defined activity types to database."""

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

    Activity(activity_1)...

    # TODO ? - flash("Great! Looks like you're ready to start tracking!")

    return redirect("/main")


@app.route("/signin", methods=["GET"])
def display_signin_form():
    """Display form for logging into existing account."""

    return render_template("signin.html")


@app.route("/signin", methods=["POST"])
def signin_user():
    """Handle sign-in."""

    # CODE

    return redirect("/main")  # After logging end, send user to main page.


# For additional routes, a stub:

# @app.route("/main")
# def ______():
#     """ DOCSTRING"""

#   CODE

#    return CODE


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    app.run()
