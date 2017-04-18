from model import db, Occurrence
from twilio.rest import Client
from flask import Flask
from datetime import datetime, timedelta
import os

# schedule to run using crontab

# for multiple commands, use && operator

# env > env/bin/python twilio-script.py

# Tell crontab to use bash, not sh:
# SHELL=/bin/bash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///tracker"
db.app = app
db.init_app(app)
db.create_all()

print "yes this ran"
# Query for phone numbers of people with incompleted occurrences
numbers_to_dial = set()
incomplete_occurrences = Occurrence.query.filter((Occurrence.end_time.is_(None) | Occurrence.after_rating.is_(None))).all()

# Create a list with the phone number for each user who has an incomplete
# occurrence scheduled to have started over 24 hours ago. This is for an SMS
# reminder to open the app and complete their entry, given that they should have
# completed the activity and have had enough time to remember to document it at
# this point (while not having, yet, forgotten how they felt about it).
for occurrence in incomplete_occurrences:
    if occurrence.activity.user.phone_number and occurrence.start_time < (datetime.now() - timedelta(hours=24)):
        numbers_to_dial.add(occurrence.activity.user.phone_number)

account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

client = Client(account_sid, auth_token)

for number in numbers_to_dial:
    message = client.messages.create(
        to=number,
        from_="+19073121980",
        body="""Hey friend! Looks like you've got one or more planned activities you might have finished. Let's hear how you felt, while it's still fresh in your mind!""")

    print(message.sid)
