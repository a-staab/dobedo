import unittest
from server import app
from model import db, connect_to_db, example_data


class Test(unittest.TestCase):

    def setUp(self):
        """Do this before each test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///test_database")

        # Create tables and add sample data
        db.create.all()
        example_data()

    def tearDown(self):
        """Do this after every test."""

        db.session.close()
        db.drop_all()


class Test_Signed_In(Test):

    def setUp(self):
        """Do this before each test."""

        super(Test, self).setUp()   # Get more info

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def t_request_activity_types(self):

        result = self.client.get("/setup")
        self.assertEqual(result.status_code, 200)
        self.assertIn('usually ideal', result.data)

    def t_create_activity_types(self):

        result = self.client.post("/setup", data={"activity_type": "coding",
                                  "user_id": "session[\"user_id\"]"},
                                  follow_redirects=True)
        # Change 'Results' below once final copy and data viz are complete
        self.assertIn('Results', result.data)

    # def t_create
    # # Test activity setup, which requires session data
    # active_activity = Activity(activity_type='coding',
    #                            user_id=session["user_id"])

    # # Test is_active can be specified too (though this change wouldn't normally
    # # be set at creation time)
    # inactive_activity = Activity(activity_type='coding',
    #                              user_id=session["user_id"],
    #                              is_active=False)
if __name__ == '__main__':
    unittest.main()
