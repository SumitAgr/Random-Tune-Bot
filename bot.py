# Reddit PRAW library
import praw
from praw.exceptions import APIException
import prawcore

# Twitter Python wrapper
import tweepy

# Config file
import config

# Importing time libraries
import time
from datetime import datetime
from pytz import timezone

# Adding US East timezone
est_timezone = timezone('US/Eastern')

# Random library
import random

# TinyDB library to store data in a JSON file
from tinydb import TinyDB, Query
db = TinyDB('db.json')

# Adding twitter developer credentials
auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

# Authenticating twitter
api = tweepy.API(auth)
print("Logged into Twitter")

# Adding reddit developer credentials
def bot_login():
    bot_login_info = praw.Reddit(username = config.REDDIT_USERNAME,
                password = config.REDDIT_PASSWORD,
                client_id = config.REDDIT_CLIENT_ID,
                client_secret = config.REDDIT_CLIENT_SECRET,
                user_agent = config.REDDIT_USERAGENT)
    
    print(f"Logged into Reddit as {bot_login_info.user.me()}")
    
    return bot_login_info

# Main function to get the random tune from reddit submissions and then filtering youtube URLs. 
# Also checks if the tune has been posted and if it has, randomizes the list until new random tune 
def get_random_tune(bot_login_info):
    '''
    The function takes top submissions from the specificed subreddits and then filters them for youtube links only.
    After appending it to the created list, the list is randomized into a lambda function.
    It then checks with the json file if it has been used, if it is used, it loops until a new non-used tune is found.
    After getting the tune, the tune is posted to Twitter.
    '''

    list_of_submissions = []
    
    for submission in bot_login_info.subreddit('listentothis+music+hiphopheads').hot(limit = 50):
        if 'youtube.com/' in submission.url:
            list_of_submissions.append(submission.url)
        elif 'youtu.be/' in submission.url:
            list_of_submissions.append(submission.url)
        else:
            pass
    
    tune_randomizer = lambda: random.choice(list_of_submissions)
    
    never_used = False
    while not never_used:
        tune_randomizer_variable = tune_randomizer()
        if db.contains(Query()['tune'] == tune_randomizer_variable) == False:

            db.insert({'tune': tune_randomizer_variable})

            est_time = datetime.now(est_timezone)
            print(est_time.strftime("%c"))
            print(f"Posting to Twitter - {tune_randomizer_variable}")
            
            api.update_status(f"{est_time.strftime('Here is your random tune for %A! The current time is %X')} \n {tune_randomizer_variable}")

            never_used = True

            if never_used:
                continue
        else:
            pass

# While loop to continuously run the function every 4 hours
while (True):
    get_random_tune(bot_login())
    print("Sleeping for 4 hours!")
    time.sleep(14400)