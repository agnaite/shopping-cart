from controller import app, ProductsController, UsersController, CartProductsController

class Store(object):
    """A store"""

    def get_user(self, email):
        """Retrieve User."""

        return UsersController.show(email)

    def add_user(self, email):
        """Add User to the database."""

        return UsersController.create(email)

    def add_product(self, title, price, available_inventory):
        """Add Product to the database"""

        return ProductsController.create(title, price, available_inventory)

    def get_products(self):
        """Get all the products."""

        return ProductsController.index()

    def get_product(self, title):
        """Get a product based on title."""

        return ProductsController.show(title)

    def get_cart(self, user):
        """Return list of items in a User's Cart."""

        return CartProductsController.index(user)

    def add_to_cart(self, user, product, quantity):
        """Add Product to Cart."""

        return CartProductsController.create(user, product, quantity)

    #
    # def remove_from_cart(self, user, product):
    #     """Remove Product from Cart."""
    #
    #     # get the items in user's cart
    #     user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()
    #
    #     if user_cart:
    #         # get the product to be removed from user's cart
    #         product_to_remove = CartProduct.query.filter_by(cart_id=user_cart.cart_id,
    #                                                         product_id=product.product_id).first()
    #         if product_to_remove:
    #             db.session.delete(product_to_remove)
    #             db.session.commit()
    #             print "Product removed from cart."
    #             return product_to_remove
    #         else:
    #             print "Product not found."
    #             return None
    #     else:
    #         print "Your cart is empty."
    #         return None
    #
    # def update_quantity_in_cart(self, user, product, new_quantity):
    #     """Update the quantity of a Product in User's Cart."""
    #
    #     user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()
    #     if user_cart:
    #         # get the product to be updated from user's cart
    #         product_to_update = CartProduct.query.filter_by(cart_id=user_cart.cart_id,
    #                                                         product_id=product.product_id).first()
    #         if product_to_update and product_to_update.product.available_inventory >= new_quantity:
    #             product_to_update.quantity = new_quantity
    #             db.session.commit()
    #             print "Product quantity updated."
    #             return product_to_update
    #         else:
    #             print "Product not found or quantity requested exceeds product's inventory."
    #             return None
    #
    #     return None
    #
    # def checkout_cart(self, user):
    #     """Checkout cart_products and mark Cart as complete."""
    #
    #     user_cart = Cart.query.filter_by(user_id=user.user_id, complete=False).first()
    #
    #     # if there is an active carts that contains products,
    #     # iterate over each product in active cart,
    #     # check that inventory is still greater than quantity in cart,
    #     # and update product's available inventory
    #     if user_cart and user_cart.cart_products:
    #         for product in user_cart.cart_products:
    #             if product.quantity <= product.product.available_inventory:
    #                 product.product.available_inventory -= product.quantity
    #             else:
    #                 print "Quantity requested for {} exceeds the inventory. Sorry!".format(product.product.title)
    #                 self.update_quantity_in_cart(user, product, product.product.available_inventory)
    #                 return user_cart
    #
    #         # mark cart as complete and add checkout timestamp
    #         user_cart.complete = True
    #         user_cart.cart_completed = datetime.now()
    #         db.session.commit()
    #         print "Thank you for shopping."
    #         return user_cart.cart_products
    #     else:
    #         print "Your cart is empty."
    #         return None
    #
    # def view_purchase_history(self, user):
    #     """Display all completed orders for a User."""
    #
    #     completed_orders = Cart.query.filter_by(user_id=user.user_id, complete=True).all()
    #
    #     for completed_order in completed_orders:
    #         print '-' * 36
    #         print "Order ID: {}".format(completed_order.cart_id)
    #         print "Order date: {}".format(completed_order.cart_completed.strftime("%x %X"))
    #
    #         for product in completed_order.cart_products:
    #             print "[{}] {}: ${:4,.2f}".format(product.product_id,
    #                                               product.product.title,
    #                                               product.product.price * product.quantity)
    #
    #     if not completed_orders:
    #         print "No orders found for {}.".format(user.email)
    #
    # def get_purchase_history(self, user):
    #     """Return list of completed orders."""
    #
    #     completed_orders = Cart.query.filter_by(user_id=user.user_id, complete=True).all()
    #     return completed_orders


if __name__ == "__main__":

    from model import connect_to_db
    connect_to_db(app)

    # create an instance of store
    store = Store()
    user = store.get_user("agne@gmail.com")
    product = store.get_product("The Cotton Crew")

    print "Use 'store' to invoke methods."
