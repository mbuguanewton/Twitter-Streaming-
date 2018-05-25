from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

#create a class
class TwitterStreamer():
    # class for streaming and process live tweets
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #handles twitter authentication and the connection to the twitter steaming API
        listener = StdOutListener()
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

class StdOutListener(StreamListener):
    # basic listener clss that prints received tweers 
    def __inti__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
    
    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    hash_tag_list = ['NYS scandal', 'nairobi scandals', 'ruto', 'nys']
    fetched_tweets_filename = 'tweets.json'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
  