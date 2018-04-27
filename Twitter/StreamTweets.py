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

users, IDs = np.loadtxt('users.txt', dtype = str, unpack = True, delimiter = ',')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_status(self, data): #on_data ¿?
		data = json.loads(data)

		date = data['created_at']
		ID = data['id']
		name = data['user']['screen_name']
		user_id = data['user']['id'],

#		print name, user_id, data['retweeted']
#		sys.exit()

		if data['truncated'] == True:	tweet = data['extended_tweet']['full_text']
		else: tweet = data['text']

		JSON = {'tweet' : tweet, 'date': date, 'ID': ID}


		if user_id in IDS:
			collection.insert_one(JSON)

        return True

    def on_error(self, status):
   	    print 'Error: ' status

#for i in range(len(users)):
#	collection = db[users[i]]


#usuario = [str(IDs[2])]
#print users[2]

if __name__ == '__main__':

	client = MongoClient()
	db = client['tweets']
	collection = db['test']


    #This handles Twitter authetification and the connection to Twitter Streaming API
    myStreamer = StdOutListener()
	api = authenticate()
    stream = Stream(auth = api.auth , listener = myStreamer).filter( follow = usuario, track = ['bitcoin', 'BTC'], async = True)

#	with open('file_name.json', 'w') as f:
#        json.dump(stream,f,indent=1)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
 
