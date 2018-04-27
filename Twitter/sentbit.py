import tweepy
import json
import numpy as np
from pymongo import MongoClient
import sys
import datetime

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API 
access_token = '63309916-rjMPGMnWh7Krr2Ckz0CN1hSsrhyqKfn9VwqHkK8fI'
access_secret = 'CvS4IJM6ubRkUnwAEIIqIBvP5KOhTEEQkcnC4rVE2gqmS'
consumer_key = 'SVyMrNbf2lbpPeoEJIJy94qkp'
consumer_secret = 'OlqFU4SKfU3AcxyoTnGmuSrPCTpP99dIiJPJvo99a048qIRyK2'

users = np.loadtxt('users.txt', dtype = str)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

client = MongoClient()
db = client['tweets']

for status in tweepy.Cursor(api.user_timeline, screen_name=str(users[0])).items(1):
	print status.text

#user = api.get_user(users[0])
#for tweet in public_tweets:
#    print tweet.text







