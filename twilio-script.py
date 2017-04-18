from model import db, Occurrence
from twilio.rest import Client

# schedule to run using crontab

# for multiple commands, use && operator

# env > env/bin/python twilio.python

# Tell crontab to use bash, not sh:
    # SHELL=/bin/bash

# query for phone numbers of people with unfinished occurrences

numbers_to_dial = set()
incomplete_occurrences = Occurrence.query.filter((Occurrence.end_time.is_(None) | Occurrence.after_rating.is_(None))).all()

for occurrence in incomplete_occurrences:
    if occurrence.activity.user.phone_number:
        numbers_to_dial.add(occurrence.activity.user.phone_number)

# Your Account SID from twilio.com/console
account_sid = "ACae07e8d9c33fae8613b214c288ac637c"
# Your Auth Token from twilio.com/console
auth_token = "d49e0ff0fe2b2f738c6a50544e2b9a33"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+15108330326",
    from_="+19073121980",
    body="Hi Amber! You're off to a great start!")

print(message.sid)

# sqlalchemy homework - create an app (connect_to_db)
# flash messages??
