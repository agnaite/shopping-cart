from model import User, Product, connect_to_db, db
from app import app


def load_users():
    """Load users from user_mock_data into database."""

    print "Loading Users"

    for i, row in enumerate(open("data/mock_user_data.csv")):
        row = row.rstrip()
        user_id, email, password = row.split(",")

        user = User(email=email)

        db.session.add(user)

    db.session.commit()


def load_products():
    """Load products from product_mock_data into database."""

    print "Loading Products"

    for i, row in enumerate(open("data/mock_product_data.csv")):
        row = row.rstrip()
        title, price, inventory = row.split(",")

        product = Product(title=title,
                          price=price,
                          available_inventory=inventory)

        db.session.add(product)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_products()
