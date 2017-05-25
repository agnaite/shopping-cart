class UsersView(object):
    """The User View."""

    def create(self, user):
        """Display new user."""

        print "User with email {} added.".format(user.email)


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

    def create(self, product):
        """Display new product."""

        print "{} added".format(product.name)