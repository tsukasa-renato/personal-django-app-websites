# QuickStart

### Requirements
Python 3.X

### Install dependencies
Clone the project on your machine, open terminal in the project directory and types:

```pip install -r requirements.txt```

### Migrations
Verify whether the project is working, in the terminal, types:

```python manage.py migrate```

### Create a admin user
Create a user to access the database, types:

```python manage.py createsuperuser```

Set username, email and password.

### Test
Verify whether the project is OK, types:

```python manage.py test websites.tests.test_model```
```python manage.py test websites.tests.test_view```

Config the selenium to execute tests using selenium.

```python manage.py test websites.tests.test_selenium```

### Run the server
Run server, types:

```python manage.py runserver```

### Register a website
To register a website, access the admin page using the url ```/admin/```, access the websites model and register an 
url, and a title, click in the save, now, you can access the website using the url registered.

# About
This project was proposed just to explore the Django tool, and just as an effort to create a flexible business logic that adapts to the complexity of the product and the local.
In the case of the product, for example, the project considers a product as a result of a set of customizable options, each product can have many groups and each group can have many options.
The products, groups, options have some parameters that set how the price will be calculated, in other words, these parameters are combined to generate the final price (e.g. price type field).
You can see the website adapting as you will registering banners, categories, products, and others.
This project intends to be simple, no authentication or payment systems were created, the database used is the PostgreSQL, the focus was on the logic of the products, validations, and tests.
