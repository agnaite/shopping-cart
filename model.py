from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
import helpers

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

    @classmethod
    def index(self, user):
        """Return products in Cart."""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if cart:
            return cart.cart_products

        return None

    @classmethod
    def create(self, user, product, quantity):
        """Add CartProduct to database."""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if not cart:
            cart = Cart(user_id=user.user_id,
                        cart_created=datetime.now(),
                        complete=False)

            db.session.add(cart)
            db.session.commit()

        if product.available_inventory > 0:
            cart_product = CartProduct(product_id=product.product_id,
                                       cart_id=cart.cart_id,
                                       quantity=quantity,
                                       price=product.price,
                                       tax=helpers.get_tax_rate())

            db.session.add(cart_product)
            db.session.commit()

            return cart_product
        else:
            return None

    @classmethod
    def delete(self, user, product):

        # get the items in user's cart
        user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if user_cart:
            # get the product to be removed from user's cart
            product_to_remove = CartProduct.query.filter_by(cart_id=user_cart.cart_id,
                                                            product_id=product.product_id).first()
            if product_to_remove:
                db.session.delete(product_to_remove)
                db.session.commit()
                return product_to_remove

        return None

    @classmethod
    def update(self, user, product, new_quantity):
        """Update Product quantity in Cart."""

        user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if user_cart:
            # get the product to be updated from user's cart
            product_to_update = CartProduct.query.filter_by(cart_id=user_cart.cart_id,
                                                            product_id=product.product_id).first()

            if product_to_update and product_to_update.product.available_inventory >= new_quantity:
                product_to_update.quantity = new_quantity
                db.session.commit()
                return product_to_update

        return None

    @classmethod
    def complete(self, user):
        """Mark User's Cart as complete."""

        user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        # if there is an active carts that contains products,
        # iterate over each product in active cart,
        # check that inventory is still greater than quantity in cart,
        # and update product's available inventory
        if user_cart and user_cart.cart_products:
            for product in user_cart.cart_products:
                if product.quantity <= product.product.available_inventory:
                    product.product.available_inventory -= product.quantity
                else:
                    self.update(user, product, product.product.available_inventory)
                    return "error"

            # mark cart as complete and add checkout timestamp
            user_cart.complete = True
            user_cart.cart_completed = datetime.now()
            db.session.commit()
            return user_cart
        else:
            return None

    @classmethod
    def show_completed(self, user):
        """Get completed orders for user."""

        return Cart.query.filter_by(user_id=user.user_id, complete=True).all()

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
