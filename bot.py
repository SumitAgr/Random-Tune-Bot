import praw
from praw.exceptions import APIException
import prawcore

import tweepy

import config

import schedule
import time

import random

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
print("Logged into Twitter")

def bot_login():
    bot_login_info = praw.Reddit(username = config.REDDIT_USERNAME,
                password = config.REDDIT_PASSWORD,
                client_id = config.REDDIT_CLIENT_ID,
                client_secret = config.REDDIT_CLIENT_SECRET,
                user_agent = config.REDDIT_USERAGENT)
    
    print(f"Successfully logged in the bot as {bot_login_info.user.me()}")
    
    return bot_login_info

def get_randomtune_list():
    with open("posted_tunes.txt", "r") as file:
        posted_tunes = file.read()
        posted_tunes = posted_tunes.split("\n")
    
    return posted_tunes

random_tune_file = get_randomtune_list()

def get_random_tune(bot_login_info):
    list_of_submissions = []
    
    for submission in bot_login_info.subreddit('listentothis+music').hot(limit = 25):
        if 'youtube.com/' in submission.url:
            list_of_submissions.append(submission.url)
        elif 'youtu.be/' in submission.url:
            list_of_submissions.append(submission.url)
        else:
            pass
    
    tune_randomizer = random.choice(list_of_submissions)
    
    print(time.strftime("%c"))
    print(f"Posting to Twitter - {tune_randomizer}")
    api.update_status(f"{time.strftime('%c')} \n {tune_randomizer}")

    return tune_randomizer

    # with open("posted_tunes.txt", "a") as file:
    #     file.write(tune_randomizer + "\n")

    # if tune_randomizer in random_tune_file:
    #     new_random_tune = random.choice(list_of_submissions)
        
    #     with open("posted_tunes.txt", "a") as file:
    #         file.write(new_random_tune + "\n")
        
    #     return new_random_tune
    # else:
    #     return tune_randomizer

# random_tune = get_random_tune(bot_login())

# def post_to_twitter():
#     print(time.strftime("%c"))
#     print(f"Posting to Twitter - {random_tune}")
#     api.update_status(f"{time.strftime('%c')} \n {random_tune}")

# schedule.every(1).minutes.do(post_to_twitter)

while (True):
    get_random_tune(bot_login())
    time.sleep(60)