from model import User, connect_to_db, db
from app import app

def load_users():
    """Load users from user_mock_data into database."""

    print "Users"

    for i, row in enumerate(open("data/MOCK_USER_DATA.csv")):
        row = row.rstrip()
        user_id, email, password = row.split(",")

        user = User(email=email)

        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    # set_val_user_id()