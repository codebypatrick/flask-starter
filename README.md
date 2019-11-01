## Introduction
This is a Flask boilerplate. The purpose of this project is to get you started Quick and Easy.

## Built with
* [Flask](http://flask.pocoo.org) - The web framework
* [Tailwind css](https://tailwind.com) - Styling utilities

## Features
* Authentication and authorization 
* User management
* Page Management
* Blog Management
* Rest api for frontend app development (mobile, electron etc) 

## Prerequisites
* Python 
* npm

## Get started
Clone the git repo
```bash
$ git clone http://github.com/codebypatrick/project.git
```
Setup Python, virtualenv and install dependencies
```bash
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Setup Database and Migrations
``` bash
$ python manage.py db init
$ python manage.py db migrate -m 'Initial database setup'
$ python manage.py db upgrade
#TODO add seed function
```
Run the server
```bash
# set enviroment variables (development, production, testing)
$ export APP_SETTINGS='development' 
#run server
$ python run.py
```
This will initiate a developement server runing on port 5000 visit the site by going to the URL:

```bash 
http://localhost:5000
```

## Deployment
TODO

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Patrick Mukasa - <codebypatrick@gmail.com>

Project Link: [https://github.com/codebypatrick/flask-starter.git](https://github.com/codebypatrick/flask-starter.git)
