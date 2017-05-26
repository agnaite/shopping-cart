# Shopping Cart

A simple shopping cart system.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites

- PostgreSQL
- Python 2.7

### Installing

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/agnaite/shopping-cart.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database "store".
```
$ createdb store
```
Create your database tables and seed example data.
```
$ python model.py
$ python seed.py
```
Run the app from the command line in interactive mode.
```
$ python -i app.py
```
<!---
### Running the tests

Create database "testdb".
```
$ createdb testdb
```
Run the tests script from the command line.
```
$ python tests.py
```
-->
### Store methods

All methods below will be called on a `Store()` instance.

* `add_user(email)`: Adds a User to the database. Returns the User object.
* `get_user(email)`: Get a user based on the email address. Returns the User object.
* `add_product(title, price, available_inventory)`: Adds a Product to the database. Returns the Product object.
* `get_products()`: View all the available Products.
* `get_product(title)`: Returns Product based on title.
* `get_cart(user)`: Get a list of CartProducts for a specific User object passed in.
* `add_to_cart(user, product, quantity)`: Adds a Product to a User's cart. Takes in a User object, a Product object, and quantity.
* `remove_from_cart(user, product)`: Removes a Product from a User's Cart. Takes in a User and a Product object.
* `update_quantity_in_cart(user, product, new_quantity)`: Updates the quantity for a specific Product in a User's cart. Takes in a User object, a Product object, and the new quantity.
* `checkout_cart(user)`: Completes purchase and checks out a specific User's cart. Cart gets marked as complete. Takes in a User object.
* `get_purchase_history(user)`: Get a list of all the Cart objects for a specific User that have been completed. Takes in a User object.

### Basic usage example

```
python -i app.py
Use 'everlane' to invoke methods.
>>> user = User.get_user("taylor@everlane.com")
>>> user
<User user_id=105 email=taylor@everlane.com>
>>> everlane.view_cart(user)
Your cart is empty.
Total: $0.00
>>> everlane.get_products()
[1] The Pointed Slide (78): $145.00.
[14] The Linen Box-Cut Tee (987): $35.00.
[15] The Cotton Crew (100): $20.00.
[16] The Drape Trench Coat (50): $138.00.
[17] The Slouchy Chino Pant (80): $58.00.
[18] The Linen Shirt Dress (100): $78.00.
[19] The Modern Babo (30): $145.00.
[20] The City Anorak (80): $88.00.
[21] The Modern Loafer (50): $168.00.
[22] The Relaxed Cotton Shirt (80): $65.00.
[25] The Petra Market (40): $365.00.
[26] The Foldover Pouch (100): $98.00.
[27] The Long Zip Wallet (60): $120.00.
[24] The GoWeave Track Pant (199): $81.00.
>>> cotton_crew = everlane.get_product("The Cotton Crew")
>>> cotton_crew                                                                                   
<Product product_id=1 title=The Cotton Crew>
>>> everlane.add_to_cart(user, cotton_crew, 1)
The Cotton Crew added to cart.
>>> everlane.view_cart(user)
[1] The Cotton Crew (1): $20.00, tax: $2.00.                                                      
Total: $22.00
>>> everlane.checkout_cart(user)
Thank you for shopping.
>>> everlane.view_cart(user)
Your cart is empty.
Total: $0.00
>>> everlane.get_purchase_history(user)
------------------------------------
Order ID: 9
Order date: 05/26/17 10:14:06
[1] The Cotton Crew: $20.00
```

