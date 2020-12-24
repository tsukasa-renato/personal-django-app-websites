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

```python manage.py tests```

### Run the server
Run server, types:

```python manage.py runserver```

### Register a website
To register a website, access the admin page using the url ```/admin/```, access the websites model and register an 
url, and a title, click in the save, now, you can access the website using the url registered.
