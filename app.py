from flask import Flask
from model import connect_to_db, db, User, Product, Cart, CartProduct
from datetime import datetime

app = Flask(__name__)


class Store(object):
    """A store"""

    def add_user(self, email):
        """Add User to the database."""

        try:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

            print "User added."
            return user
        except:
            print "User already exists."
            return None

    def add_product(self, title, price, available_inventory):
        """Add Product to the database"""

        product = Product(title=title,
                          price=price,
                          available_inventory=available_inventory)

        db.session.add(product)
        db.session.commit()

        print "Product added."
        return product

    def view_products(self):
        """Print all the products in inventory."""

        products = Product.query.all()

        for product in products:
            if product.available_inventory > 0:
                print "[{}] {} ({}): ${:4,.2f}.".format(product.product_id,
                                                        product.title,
                                                        product.available_inventory,
                                                        product.price)

    def get_products(self):
        """Return all the Products in inventory."""

        products = Product.query.all()
        return products

    def view_cart(self, user):
        """List Products in User's cart."""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()
        total = 0

        if cart:
            for item in cart.cart_products:

                product = Product.query.get(item.product_id)
                subtotal = product.price * item.quantity
                total += subtotal

                print "[{}] {} ({}): ${:4,.2f}.".format(product.product_id,
                                                        product.title,
                                                        item.quantity,
                                                        subtotal)
        else:
            print "Your cart is empty."

        print "Total: ${:4,.2f}".format(total)

    def get_cart(self, user):
        """Return list of items in a User's Cart."""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if cart:
            return cart.cart_products

    def add_to_cart(self, user, product, quantity):
        """Add Product to Cart."""

        cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        # if user does not have an active cart, make a cart
        if not cart:
            cart = Cart(user_id=user.user_id,
                        cart_created=datetime.now(),
                        complete=False)

            db.session.add(cart)
            db.session.commit()

        # if product's inventory is greater than zero,
        # create an instance of cart_product
        if product.available_inventory > 0:
            cart_product = CartProduct(product_id=product.product_id,
                                       cart_id=cart.cart_id,
                                       quantity=quantity)

            db.session.add(cart_product)
            db.session.commit()
            print "Product added."
            return cart_product

        else:
            print "Out of stock."
            return None

    def remove_from_cart(self, user, product):
        """Remove Product from Cart."""

        # get the items in user's cart
        user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()

        if user_cart:
            # get the product to be removed from user's cart
            product_to_remove = CartProduct.query.filter_by(cart_id=user_cart.cart_id,
                                                            product_id=product.product_id).first()
            if product_to_remove:
                db.session.delete(product_to_remove)
                db.session.commit()
                print "Product removed from cart."
                return product_to_remove
            else:
                print "Product not found."
                return None
        else:
            print "Your cart is empty."
            return None

    def update_quantity_in_cart(self, user, product, new_quantity):
        """Update the quantity of a Product in User's Cart."""

        user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()
        if user_cart:
            # get the product to be updated from user's cart
            product_to_update = CartProduct.query.filter_by(cart_id=user_cart.cart_id,
                                                            product_id=product.product_id).first()
            if product_to_update and product_to_update.product.available_inventory >= new_quantity:
                product_to_update.quantity = new_quantity
                db.session.commit()
                print "Product quantity updated."
            else:
                print "Product not found or quantity requested exceeds product's inventory."

    def checkout_cart(self, user):
        """Checkout cart_products and mark Cart as complete."""

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
                    print "Quantity requested for {} exceeds the inventory. Sorry!".format(product.product.title)
                    self.update_quantity_in_cart(user, product, product.product.available_inventory)
                    return

            # mark cart as complete and add checkout timestamp
            user_cart.complete = True
            user_cart.cart_completed = datetime.now()
            db.session.commit()
            print "Thank you for shopping."
        else:
            print "Your cart is empty."

    def view_purchase_history(self, user):
        """Display all completed orders for a User."""

        completed_orders = Cart.query.filter_by(user_id=user.user_id, complete=True).all()

        for completed_order in completed_orders:
            print '-' * 36
            print "Order ID: {}".format(completed_order.cart_id)
            print "Order date: {}".format(completed_order.cart_completed.strftime("%x %X"))

            for product in completed_order.cart_products:
                print "[{}] {}: ${:4,.2f}".format(product.product_id,
                                                  product.product.title,
                                                  product.product.price * product.quantity)

        if not completed_orders:
            print "No orders found for {}.".format(user.email)

    def get_purchase_history(self, user):
        """Return list of completed orders."""

        completed_orders = Cart.query.filter_by(user_id=user.user_id, complete=True).all()
        return completed_orders


if __name__ == "__main__":

    connect_to_db(app)

    # create an instance of store
    store = Store()
    # grab user with id 1
    user = User.query.get(1)

    print "Use 'store' to invoke methods."
