from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

db = SQLAlchemy()


#############################################################################
# Model definitions

class User(db.Model):
    """User of shopping website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)

    @classmethod
    def create(self, email):
        """Add new User to database."""

        user = User(email=email)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return None

        return user

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Cart(db.Model):
    """An cart and its state."""

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cart_created = db.Column(db.DateTime)
    cart_completed = db.Column(db.DateTime)
    complete = db.Column(db.Boolean)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("carts", order_by=cart_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Cart cart_id=%s user_id=%s is complete=%s>" % (self.cart_id,
                                                                self.user_id,
                                                                self.complete)


class Product(db.Model):
    """A product"""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    price = db.Column(db.Float(precision=2))
    title = db.Column(db.String(255), nullable=False)
    available_inventory = db.Column(db.Integer, nullable=False)

    @classmethod
    def create(self, title, price, available_inventory):
        """Create new product."""

        product = Product(title=title,
                          price=price,
                          available_inventory=available_inventory)

        db.session.add(product)
        db.session.commit()

        return product

    @classmethod
    def view_all(self):
        """Return all products"""

        return Product.query.all()

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Product product_id=%s title=%s>" % (self.product_id, self.title)


class CartProduct(db.Model):
    """A product in a cart."""

    __tablename__ = "cart_products"

    cart_product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"))
    quantity = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define relationship to product
    product = db.relationship("Product",
                              backref=db.backref("cart_products", order_by=cart_product_id))
    # Define relationship to cart
    cart = db.relationship("Cart",
                           backref=db.backref("cart_products", order_by=cart_product_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CartProduct cart_product_id=%s cart_id=%s user_id=%s title=%s>" % (self.cart_product_id,
                                                                                    self.cart_id,
                                                                                    self.cart.user_id,
                                                                                    self.product.title)


####################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///store'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from controller import app
    connect_to_db(app)

    # Create tables and some sample data
    db.create_all()

    print "Connected to DB."
