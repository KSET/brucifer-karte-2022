# brucifer-karte
Brucifer karte 2022 (not finished)

## Prerequisites

Before getting started you should have the following installed and running:

-  Npm - [instructions](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
-  Vue CLI 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
-  Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)

## Setup Template

```
git clone https://github.com/pavleerg/brucifer-karte.git
cd brucifer-karte
```

Setup
```
npm install
pip install -m ./requirements.txt
python manage.py migrate
```

## Running Development Servers

```
python manage.py runserver
```
Open another terminal in the repo directory:
```
cd ui
npm run serve
```

## Adjusting the environment variables

- in the ui folder, rename the .env.example to .env and ajust your enivronment variables

## Adding an admin user to be able to access the site

- got to the development server, the rest api service at http://127.0.0.1:8000/
- click on users
- at the bottom on the page your admin user
- set the id to any number
- set the privilege to "1" 
- be sure to set the same email you are gonna use for the google login

## Logging in the app

- go to http://localhost:8080/bruckarte/login/#loaded
- logg in with the email that you previously added to your admin user
