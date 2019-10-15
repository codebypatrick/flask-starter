## Website Template
This is a starter for flask web projects

## Setup
Clone repo
```bash
$ git clone https://github.com/codebypatrick/flask-starter.git
```

Setup python
```bash
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Database and migrations
Run the initialization script

```bash
$ python manage.py db init
```

Create the migration script

```bash 
$ python manage.py db migrate -m 'your message here'
```

Apply changes to database

```bash
$ python manage.py db upgrade
```

### Seed data
Setup default data
```bash
$ python manage.py setup
```

create users
```bash
$ python manage.py create_users
```
This will create 100 fake users

create posts
```bash
$ python manage.py create_posts
```

## Summary
The site should have ability to create pages, posts and have user management.

## Pages


## Posts

## Users

# Flask Starter
This is a starter template for flask projects.

## Getting started
Instructions to get you started

### Prerequistes
* Python
* Virtualenv

### Setup and install
Download or clone the project
```bash
$ git clone https://github.com/codebypatrick/flask-starter.git
```

Setup the enviroment
```bash
$ cd flask-starter			# Change into cloned directory
$ virtualenv venv			# create virtual env
$ pip install -r requirments.txt
```

Setup database
```bash
$ python manage.py db init				# Initialize migrations
$ pyhton manage.py db migrate -m 'Intial migration'
$ python manage.py db upgrade				# Create db tables
$ python manage.py setup				# Create default application records, should be changed in production
```

Seed data
```bash
$ python manage.py create_users				# Create seed users 100
$ python manage.py create_posts				# Create seed posts 100
```

Run the app
```bash
$ pyhton wsgi.py
```
