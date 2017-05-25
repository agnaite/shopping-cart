class UsersView(object):
    """The User View."""

    @classmethod
    def create(self, user):
        """Display new user."""

        if user:
            print "User with email {} added.".format(user.email)
        else:
            print "Error adding user."


class ProductsView(object):
    """The Product View."""

    @classmethod
    def index(self, products):
        """Display all products."""

        for product in products:
            if product.available_inventory > 0:
                print "[{}] {} ({}): ${:4,.2f}.".format(product.product_id,
                                                        product.title,
                                                        product.available_inventory,
                                                        product.price)

    @classmethod
    def create(self, product):
        """Display new product."""

        print "{} added".format(product.name)

class CartProductsView(object):
    """The CartProduct View."""

    @classmethod
    def index(self, cart_products):
        """Display all Cart products."""

        total = 0
        output = "[{}] {} ({}): ${:4,.2f}, tax: ${:4,.2f}."

        if cart_products:
            for cart_product in cart_products:

                product = cart_product.product
                subtotal = cart_product.price * cart_product.quantity
                tax = subtotal * cart_product.tax
                total += subtotal + tax

                print output.format(product.product_id,
                                    product.title,
                                    cart_product.quantity,
                                    subtotal,
                                    tax)
        else:
            print "Your cart is empty."

        print "Total: ${:4,.2f}".format(total)

    @classmethod
    def create(self, cart_product):
        """Display Product added to Cart."""

        if cart_product:
            print "{} added to cart.".format(cart_product.product.title)
        else:
            print "{} is out of stock.".format(cart_product.product.title)
