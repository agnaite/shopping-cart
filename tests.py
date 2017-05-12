import unittest
from app import app, Store
from model import connect_to_db, db, User
from seed import load_users, load_products


class ShoppingCartUnitTestCase(unittest.TestCase):
    """Tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        load_users()
        load_products()

        self.store = Store()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_add_user(self):
        """Test adding User."""

        # adds new user OK
        self.store.add_user("taylor@everlane.com")
        self.assertTrue(User.query.filter_by(email="taylor@everlane.com").first())

        # does not add a user if email in database
        self.assertIsNone(self.store.add_user("taylor@everlane.com"))


if __name__ == "__main__":

    unittest.main()
