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

    def remove_from_cart(self, user, product):
        """Remove Product from Cart."""

        return CartProductsController.delete(user, product)

    def update_quantity_in_cart(self, user, product, new_quantity):
        """Update the quantity of a Product in User's Cart."""

        return CartProductsController.update(user, product, new_quantity)

    def checkout_cart(self, user):
        """Checkout cart_products and mark Cart as complete."""

        return CartProductsController.complete(user)

    def get_purchase_history(self, user):
        """Display all completed orders for a User."""

        CartProductsController.show_completed(user)


if __name__ == "__main__":

    from model import connect_to_db
    connect_to_db(app)

    # create an instance of store
    everlane = Store()
    taylor = everlane.get_user("taylor@everlane.com")
    cotton_crew = everlane.get_product("The Cotton Crew")

    print "Use 'everlane' to invoke methods."
