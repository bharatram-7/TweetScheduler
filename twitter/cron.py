from .models import Integration, Post, History
from requests_oauthlib import OAuth1
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler(daemon=True)

api_key = os.environ["api_key"]
api_secret = os.environ["api_secret"]
service_url = 'https://api.twitter.com/1.1/statuses/update.json'


def post_to_twitter(post):
    # Get the credentials using user_id
    creds = Integration.objects.get(user_id=post.user_id)
    # Make the call to Twitter to post the data
    oauth = OAuth1(api_key,
                   client_secret=api_secret,
                   resource_owner_key=creds.token,
                   resource_owner_secret=creds.secret)

    data = {
        "status": post.content
    }
    r = requests.post(service_url, auth=oauth, data=data)
    if r.status_code == 200:
        try:
            History.objects.create(content=post.content, user_id=post.user_id)
            post.delete()
        except:
            pass
    else:
        print(r.content)


def fetch_records():
    posts = Post.objects.raw('SELECT t1.* FROM twitter_post AS t1 LEFT OUTER JOIN twitter_post AS t2 '
                             'ON t1.user_id = t2.user_id AND t1.id > t2.id WHERE t2.user_id is NULL;')
    if len(posts) > 0:
        print("Greater than 1")
        for post in posts:
            post_to_twitter(post)


scheduler.add_job(fetch_records, 'cron', minute='*')
scheduler.start()
