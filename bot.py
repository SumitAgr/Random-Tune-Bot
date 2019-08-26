# Reddit PRAW library
import praw
from praw.exceptions import APIException
import prawcore

# Twitter Python wrapper
import tweepy

# Config file
import config

# Importing time library
import time

# Random library
import random

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
    
    print(f"Successfully logged in the bot as {bot_login_info.user.me()}")
    
    return bot_login_info

# Txt file to store random tunes that the bot has tweeted
def get_randomtune_list():
    with open("posted_tunes.txt", "r") as file:
        posted_tunes = file.read()
        posted_tunes = posted_tunes.split("\n")
    
    return posted_tunes

# Initializing a variable
random_tune_file = get_randomtune_list()

# Main function to get the random tune from reddit submissions and then filtering youtube URLs. 
# Also checks if the tune has been posted and if it has, randomizes the list until new random tune 
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
    
    with open("posted_tunes.txt", "a") as file:
        file.write(tune_randomizer + "\n")

    if tune_randomizer in random_tune_file:
        new_random_tune = random.choice(list_of_submissions)
        
        with open("posted_tunes.txt", "a") as file:
            file.write(new_random_tune + "\n")
        
        print(time.strftime("%c"))
        print(f"Posting to Twitter - {new_random_tune}")
        api.update_status(f"{time.strftime('Here is your random tune for %A! The current time is %X')} \n {new_random_tune}")
    else:
        print(time.strftime("%c"))
        print(f"Posting to Twitter - {tune_randomizer}")
        api.update_status(f"{time.strftime('Here is your random tune for %A! The current time is %X')} \n {tune_randomizer}")

# While loop to continuously run the function every 4 hours
while (True):
    get_random_tune(bot_login())
    time.sleep(14400)