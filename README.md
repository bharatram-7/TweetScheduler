# TweetScheduler

A simple application that integrates with Twitter to post your tweets at regular intervals.

## Prerequisities

Since the application involves an integration with Twitter, you need to register a new app in Twitter's developer portal.

Make note of the following parameters from the app you create: 

- Api Key
- Api Secret

These are required to let twitter know that your registered app is posting tweets on behalf of the users.

All required libraries are in requirements.txt file.

## Features

### v1

- Tweets your content at regular intervals using django-crontab

### v2

- Added REST API support
- Used Vue.js and axios for a slightly better experience

## Getting Started

### Cloning the Repository

Create a working directory on your device and run the command below to clone the repository.

```
git clone https://github.com/bharatram-7/TweetScheduler.git
```

### Running the application

- If you are running this code in staging, set "DEBUG = True" in Scheduler --> Settings.py

- Irrespective of whether it's run in staging/production, the following environment variables need to be set:

```
export api_key='YOUR_APP'S_API_KEY'
export api_secret='YOUR_APP'S_API_SECRET'
export django_secret='DJANGO_SECRET_IN_SETTINGS.PY'
export EMAIL_HOST_USER='YOUR_EMAIL_ADDRESS'
export EMAIL_HOST_PASSWORD='EMAIL_ADDRESS_PASSWORD'
```
- To run the server, 

```
python manage.py runserver
```

#### Please note that Django-crontab works only in Mac or Linux systems
