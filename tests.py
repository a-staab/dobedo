import unittest
from server import app
from model import db, connect_to_db, example_data


class Test(unittest.TestCase):

    def setUp(self):
        """Do this before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///test_database")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do this after every test."""

        db.session.close()
        db.drop_all()

    def test_signup_page_render(self):
        """Tests that signup page loads."""

        result = self.client.get("/signup")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Create your", result.data)

    def test_signin_page_render(self):
        """Tests that sign-in page loads."""

        result = self.client.get("/signin")
        self.assertEqual(result.status_code, 200)
        self.assertIn("to your account", result.data)

    # def test_create_new_user(self):
    #     """Tests database for existence of user created using create_new_user
    #     helper function."""

    #     result = User.query.filter(User.email == 'hb-student@hackbright.com').one()
    #     self.assertIn('with user_id', result.data)


class Test_Signed_In(Test):

    def setUp(self):
        """Do this before each test."""

        super(Test_Signed_In, self).setUp()

        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do this after every test."""

        super(Test_Signed_In, self).tearDown()

    def test_request_activity_types(self):
        """Tests activity setup page loads."""

        result = self.client.get("/setup")
        self.assertEqual(result.status_code, 200)
        self.assertIn('usually ideal', result.data)

    def test_create_activity_types(self):
        """Tests user can specify an activity type for tracking from setup page.
        """

        result = self.client.post("/setup",
                                  data={"activity_1": "coding",
                                        "activity_2": "",
                                        "activity_3": "",
                                        "activity_4": "",
                                        "activity_5": "",
                                        "activity_6": "",
                                        "activity_7": "",
                                        "activity_8": "",
                                        "activity_9": "",
                                        "activity_10": ""},
                                  follow_redirects=True)
        # Change 'Results' below once final copy and data viz are complete
        self.assertIn('Results', result.data)

    def test_main_page_render(self):
        """Tests that main page loads."""

        result = self.client.get("/main")
        self.assertEqual(result.status_code, 200)
        self.assertIn("activity to begin tracking", result.data)


if __name__ == '__main__':
    unittest.main()
