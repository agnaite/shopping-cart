# Shopping Cart

A simple shopping cart system.

## Getting Started

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
<!-- 
## Running the tests

Explain how to run the automated tests for this system
 -->

### Store Methods

All methods below will be called on a `Store()` instance.

* `def add_user(email)`: Adds a User to the database. Returns the User object.
* `def add_product(title, price, available_inventory)`: Adds a Product to the database. Returns the Product object.
* `def view_products()`: Prints all the available Products.
* `def get_products()`: Returns all the available Products.
* `def view_cart(user)`: Prints the Cart contents for a specific User object passed in.
* `def get_cart(user)`: Returns a list of CartProducts for a specific User object passed in.
* `def add_to_cart(user, product, quantity)`: Adds a Product to a User's cart. Takes in a User object, a Product object, and quantity.
* `def remove_from_cart(user, product)`: Removes a Product from a User's Cart. Takes in a User and a Product object.
* `def update_quantity_in_cart(user, product, new_quantity)`: Updates the quantity for a specific Product in a User's cart. Takes in a User object, a Product object, and the new quantity.
* `def checkout_cart(user)`: Completes purchase and checks out a specific User's cart. Cart gets marked as complete. Takes in a User object.
* `def view_purchase_history(user)`: Prints all the completed orders for a specific User. Takes in a User object.
* `def get_purchase_history(user)`: Returns a list of all the Cart objects for a specific User that have been completed. Takes in a User object.

### Basic usage example

```
python -i app.py
Use 'store' to invoke methods.
>>> user = User.query.get(11)
>>> user
<User user_id=11 email=sstrauna@1688.com>
>>> store.view_cart(user)
Your cart is empty.
Total: $0.00
>>> store.view_products()
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
>>> store.add_to_cart(user, Product.query.get(21), 1)
Product added.
>>> store.view_cart(user)
[21] The Modern Loafer (1): $168.00.
Total: $168.00
>>> store.checkout_cart(user)
Thank you for shopping.
>>> store.view_cart(user)
Your cart is empty.
Total: $0.00
>>> store.view_purchase_history(user)
------------------------------------
Order ID: 12
Order date: 05/08/17 11:29:26
[21] The Modern Loafer: $168.00
```

