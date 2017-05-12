import unittest
from app import app, Store
from model import connect_to_db, db, User, Product
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

        print "Dropping testdb."

    def test_add_user(self):
        """Test adding User."""

        # adds new user OK
        self.store.add_user("taylor@everlane.com")
        self.assertTrue(User.query.filter_by(email="taylor@everlane.com").first())

        # does not add a user if email in database
        self.assertIsNone(self.store.add_user("taylor@everlane.com"))

    def test_add_product(self):
        """Test adding Product."""

        # adds new product OK
        self.store.add_product("The Elements Anorak", 148, 100)
        self.assertTrue(Product.query.filter_by(title="The Elements Anorak"))

    def test_get_products(self):
        """Test getting all the products from database."""

        # method .get_products returns all the products in the Product table
        products = self.store.get_products()
        self.assertEqual(len(products), Product.query.count())

    


if __name__ == "__main__":

    unittest.main()
