import json, datetime, credentials, sys
import numpy as np
from pymongo import MongoClient

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

def authenticate():
    try:
        consumer_key = credentials.consumer_key
        consumer_secret = credentials.consumer_secret
        access_token = credentials.access_token
        access_token_secret = credentials.access_secret

        # Connect to api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)
    except:
        print("Failed to authorize Tweepy.")
        return None

api = authenticate()

USERS, IDS = np.loadtxt('users.txt', dtype = str, unpack = True, delimiter = ',')

#Create an iterator for users

#Add since_id, max_id, iclude_rt and not mentions
for status in tweepy.Cursor(api.user_timeline, screen_name = user).items():
    print status._json['text']



