# Shopping Cart

A simple shopping cart system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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
Create database 'store'.
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
$ python -i server.py
```
<!-- 
## Running the tests

Explain how to run the automated tests for this system
 -->

### Store Methods

All methods below will be called on a `Store()` instance.

`def add_user(email)`: Adds a user to the database.
`def add_product(title, price, available_inventory)`: Adds a product to the database.
`def view_products()`: Prints all the available products.
`def view_cart(user)`: Prints the cart contents for specific user object passed in.
`def get_cart(user)`: Returns a list of CartProducts for specific user object passed in.
`def add_to_cart(user, product, quantity)`: Adds a product to a user's cart. Takes in a user object, a product object, and quantity.
`def remove_from_cart(user, product)`: Removes a product from a user's cart. Takes in a user and a product object.
`def update_quantity_in_cart(user, product, new_quantity)`: Updates the quantity for a specific product in a user's cart. Takes in a user object, a product object, and the new quantity.
`def checkout_cart(user)`: Completes purchase and checks out a specific user's cart. Cart gets marked as complete. Takes in a user object.
`def view_purchase_history(user)`: Prints all the completed orders for a specific user. Takes in a user object.
`def get_purchase_history(user)`: Returns a list of all the Cart objects for a specific user that have been completed. Takes in a user object.

### Basic usage example


