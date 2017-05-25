from model import connect_to_db, db, User, Product, Cart, CartProduct
from view import ProductsView, UsersView, CartProductsView
from flask import Flask

app = Flask(__name__)
# connect_to_db(app)


class UsersController(object):
    """Users Controller."""

    @classmethod
    def show(self, email):
        """Get a User based on email address."""

        return User.query.filter_by(email=email).first()

    @classmethod
    def create(self, email):
        """Create new User."""

        new_user = User.create(email)
        UsersView.create(new_user)


class ProductsController(object):
    """Products Controller."""

    @classmethod
    def index(self):
        """View all products."""

        products = Product.view_all()
        ProductsView.index(products)

    @classmethod
    def show(self, title):
        """Get Product based on name."""

        return Product.query.filter_by(title=title).first()

    @classmethod
    def create(self, title, price, available_inventory):
        """Create new Product."""

        new_product = Product.create(title, price, available_inventory)
        ProductsView.create(new_product)

class CartProductsController(object):
    """CartProduct Controller."""

    @classmethod
    def index(self, user):
        """View products in Cart."""

        cart_products = CartProduct.index(user)
        CartProductsView.index(cart_products)

    @classmethod
    def create(self, user, product, quantity):
        """Add Product to Cart."""

        cart_product = CartProduct.create(user, product, quantity)
        CartProductsView.create(cart_product)
