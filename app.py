from flask import Flask
from model import connect_to_db, db, User

app = Flask(__name__)


def add_to_cart():
    """Add something to the cart!"""

    print User.query.get(1)


if __name__ == "__main__":

    connect_to_db(app)

    # Create our tables and some sample data

    print "Connected to DB."
