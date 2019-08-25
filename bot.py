import praw
from praw.exceptions import APIException
import prawcore

import tweepy

import config

import schedule
import time

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def bot_login():
    bot_login_info = praw.Reddit(username = config.REDDIT_USERNAME,
                password = config.REDDIT_PASSWORD,
                client_id = config.REDDIT_CLIENT_ID,
                client_secret = config.REDDIT_CLIENT_SECRET,
                user_agent = config.REDDIT_USERAGENT)
    
    print(f"Successfully logged in the bot as {bot_login_info.user.me()}")
    
    return bot_login_info

def get_random_tune(bot_login_info):
    for submission in bot_login_info.subreddit('listentothis').hot(limit = 1):
        if 'youtube.com' in str(submission.url):
            return submission.url
        else:
            for submission in bot_login_info.subreddit('listentothis').hot(limit = 2):
                if 'youtube.com' in str(submission.url):
                    return submission.url

random_tune = get_random_tune(bot_login())

def post_to_twitter(random_tune):
    api.update_status(random_tune)
    # Test

# print(random_tune)

# api.update_status('Is this thing working?')

schedule.every(10).minutes.do(random_tune)

while(True):
    schedule.run_pending()
    time.sleep(1)