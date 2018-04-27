import json, datetime, credentials, sys
import numpy as np
from pymongo import MongoClient

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#client = MongoClient()
#db = client['tweets']

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

def get_latest_tweets(query, count, until):
    public_tweets = []
    api = authenticate()
    if (api):
        try:
            public_tweets = [(tweet.author.screen_name,
                          tweet.text,
                          tweet.created_at.isoformat())
                          for tweet in api.search(q=query, count=count, until = until, lang='en')]
        except:
            print("Tweepy request failed.")

    return public_tweets

#until: Returns tweets created before the given date. No tweets will be found for a date older than one week.
#Ex: 2015-10-21


#Evaluar si se puede cambiar directamente a almacenamiento en mongodb
def write_tweets_to_file(fname, tweets):
    if len(tweets) == 0:
        print("Number of tweets to write is zero.")
        return

    try:
        with open(fname, 'a') as f:
            for t in tweets:
                for a in t:
                    f.write(a+"\n")
                f.write("\n")

        print("Successfully wrote", len(tweets), "tweets")
    except:
        print("Error writing tweets to '" + fname + "'")


if __name__ == '__main__':
		
		users, IDs = np.loadtxt('users.txt', dtype = str, unpack = True, delimiter = ',')
        d = datetime.datetime.now()
        print("Getting tweets... (", d, ")")
        T = get_latest_tweets('bitcoin', 100, d)
        write_tweets_to_file('output.txt', T)



