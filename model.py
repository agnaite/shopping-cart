from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#############################################################################
# Model definitions

class User(db.Model):
    """User of shopping website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    # make secure!
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.String(15), nullable=True)
    # payment info?

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Cart(db.Model):
    """A shopping cart"""

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("carts", order_by=cart_id))


class Product(db.Model):
    """A product"""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    price = db.Column(db.Float, precision=2)
    title = db.Column(db.String(255), nullable=False)
    available_inventory = db.Column(db.Integer, nullable=False)


class CartProduct(db.Model):
    """A product in a cart."""

    __tablename__ = "cart_products"

    cart_product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"))

    # Define relationship to user
    product = db.relationship("Product",
                              backref=db.backref("cart_products", order_by=cart_product_id))
    # Define relationship to cart
    cart = db.relationship("Cart",
                           backref=db.backref("cart_products", order_by=cart_product_id))


def example_data():
    pass

####################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///shopping_cart'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from app import app
    connect_to_db(app)

    # Create tables and some sample data
    # db.create_all()
    example_data()

    print "Connected to DB."
