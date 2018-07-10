from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import twitter_credentials


# class for authentication
class Twitter_Authenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


####### Twitter Client ######
class TwitterClient():
    def __init__ (self, twitter_user=None):
        self.auth = Twitter_Authenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends,  id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,  id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets



class TwitterStreamer():
    # class for streaming and process live tweets
    def __init__(self):
        self.twitter_authenticator = Twitter_Authenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #handles twitter authentication and the connection to the twitter steaming API
        listener = Twitter_Listener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

class Twitter_Listener(StreamListener):
    # basic listener class that prints received tweets 
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)

            #with open('tweets.txt', 'w') as tweet_data:
               # json.dumps(data, tweet_data, ensure_ascii=False)
            
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs
            return False
        print(status)



if __name__ == "__main__":
    hash_tag_list = ['Product', 'Smartphone', 'Jumia Travel', 'Appliances']
    fetched_tweets_filename = 'tweets.json'

    twitter_client = TwitterClient('Jumia')
    print(twitter_client.get_user_timeline_tweets(5))
    #print(twitter_client.get_friend_list(10))
    #print(twitter_client.get_home_timeline_tweets(5))
   # twitter_streamer = TwitterStreamer()
    #TwitterStreamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    

