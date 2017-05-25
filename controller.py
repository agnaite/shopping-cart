from model import connect_to_db, db, User, Product, Cart, CartProduct
from view import ProductsView
from flask import Flask

app = Flask(__name__)
# connect_to_db(app)


class UsersController(object):
    """Users Controller."""

    def __init__(self):

        UsersView = UsersView()

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

    def create(self, title, price, available_inventory):
        """Create new Product."""

        new_product = Product.create(title, price, available_inventory)
        ProductsView.create(new_product)
