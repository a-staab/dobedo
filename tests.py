from unittest import TestCase
from server import app
from model import db, connect_to_db, example_data


class Test(TestCase):

    def setUp(self):
        """Do this before each test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///test_database")

        # Create tables and add sample data
        db.create.all()
        example_data()

    def tearDown(self):
        """Do this after every test."""

        db.session.close()
        db.drop_all()

    def t_request_activity_types(self):

        result = self.client.get("/setup")
        self.assertEqual(result.status_code, 200)
        self.assertIn('usually ideal', result.data)

    def t_create_activity_types(self):

        result = self.client.post("/setup", data={"activity_type": "rowing",
                                  "user_id": "session[\"user_id\"]"},
                                  follow_redirects=True)
        # Change 'Main Page' below once main page is built
        self.assertIn('Main Page', result.data)
