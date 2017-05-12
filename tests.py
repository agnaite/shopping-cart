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

    def test_get_cart(self):
        """Test getting the cart contents."""

        user = User.query.get(1)
        product_0 = Product.query.get(1)
        product_1 = Product.query.get(2)

        # cart is empty when no products have been added
        cart = self.store.get_cart(user)
        self.assertIsNone(cart)

        # adding two distinct products, returns two cartProducts
        self.store.add_to_cart(user, product_0, 1)
        self.store.add_to_cart(user, product_1, 1)
        cart = self.store.get_cart(user)
        self.assertEqual(len(cart), 2)

    def test_add_to_cart(self):
        """Test adding products to cart."""

        user = User.query.get(1)
        product_0 = Product.query.get(1)
        product_1 = Product.query.get(9)

        # adding product to cart with inventory < 1, returns None
        cart_product = self.store.add_to_cart(user, product_1, 1)
        self.assertIsNone(cart_product)

        # adding in stock product to cart, creates and returns the cartProduct
        cart_product = self.store.add_to_cart(user, product_0, 1)
        self.assertEqual(cart_product.product.title, Product.query.get(1).title)

    def test_remove_from_cart(self):
        """Test removing products from cart."""

        user = User.query.get(1)
        product_0 = Product.query.get(1)
        product_1 = Product.query.get(2)

        # removing product from empty cart returns None
        removed_product = self.store.remove_from_cart(user, product_0)
        self.assertIsNone(removed_product)

        # removing product that is not in the cart, returns None
        self.store.add_to_cart(user, product_1, 1)
        removed_product = self.store.remove_from_cart(user, product_0)
        self.assertIsNone(removed_product)

        # removing product that is in the cart, removes and returns the removed product
        removed_product = self.store.remove_from_cart(user, product_1)
        self.assertEqual(removed_product.product.title, Product.query.get(2).title)
        self.assertNotIn(removed_product, self.store.get_cart(user))

        # adding in stock product to cart, creates and returns the cartProduct
        cart_product = self.store.add_to_cart(user, product_0, 1)
        self.assertEqual(cart_product.product.title, Product.query.get(1).title)

if __name__ == "__main__":

    unittest.main()
