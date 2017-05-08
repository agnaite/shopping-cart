from flask import Flask
from model import connect_to_db, db, User, Product, Cart, CartProduct
from datetime import datetime

app = Flask(__name__)


class Store(object):
    """A store"""

    def add_user(self, email):
        """Add user to the database"""

        user = User(email=email)
        db.session.add(user)
        db.session.commit()

        print "User added."


    def add_product(self, title, price, available_inventory):
        """Add product to the database"""

        product = Product(title=title,
                          price=price,
                          available_inventory=available_inventory)

        db.session.add(product)
        db.session.commit()

        print "Product added."

    def view_cart(self, user):
        """List products in user's cart"""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if cart:
            cart_items = CartProduct.query.filter_by(cart_id=cart.cart_id).all()
            for item in cart_items:
                print "{} ({}): {}.".format(Product.query.get(item.product_id).title,
                                            item.quantity,
                                            Product.query.get(item.product_id).price)
        else:
            print "Your cart is empty."

    def add_product_to_cart(self, user, product, quantity):
        """Add product to cart"""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if not cart:
            cart = Cart(user_id=user.user_id,
                        cart_created=datetime.now(),
                        complete=False)

            db.session.add(cart)
            db.session.commit()

        cart_product = CartProduct(product_id=product.product_id,
                                   cart_id=cart.cart_id,
                                   quantity=quantity)

        db.session.add(cart_product)
        db.session.commit()


if __name__ == "__main__":

    connect_to_db(app)

    # create an instance of store
    store = Store()

    user = User.query.get(1)
    store.add_product("The Pointed Slide", 145, 100)

    print "Use 'store' to invoke methods."
