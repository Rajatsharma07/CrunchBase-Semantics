#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Stream
from tweepy.streaming import StreamListener
import csv

try:
    import json
except ImportError:
    import simplejson as json


from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
#Variables that contains the user credentials to access Twitter API
access_token = "798528063323697152-9zxLxUPeHRpmn583YJ0bRulPiINZnTw"
access_token_secret = "rujFHQMtZneJt9j0EtccAsviCSh32nRles6gCmBRiIRKb"
consumer_key = "IG75MUvqndRk1nDCwUTzd4GZc"
consumer_secret = "C9K6mq1YSECTiK1hT3IYLAi2NQ9mjRkwFrGYqzI7ziyPE5oRdC"

csvfile = open('my_scraped_tweets.csv','wb')

mywriter = csv.writer(csvfile)
mywriter.writerows([("tweetId", "tweetCreatedAt","tweetText","tweetUserId","tweetUserName","tweetUserAccount","hashtags")])

oauth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

#.filter(track=['python', 'javascript', 'ruby'])
# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()
#iterator = twitter_stream.statuses.filter(track="Google", language="en")

# Print each tweet in the stream to the screen
# Here we set it to stop after getting 1000 tweets.
# You don't have to set it to stop, but can continue running
# the Twitter API to collect data for days or even longer.
tweet_count = 1000
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter
    try:
        # Read in one line of the file, convert it into a json object
        if 'text' in tweet:  # only messages contains 'text' field is a tweet
            tweetId =  tweet['id']  # This is the tweet's id
            tweetCreatedAt = tweet['created_at']  # when the tweet posted
            tweetText = tweet['text']  # content of the tweet

            tweetUserId = tweet['user']['id']  # id of the user who posted the tweet
            tweetUserName = tweet['user']['name']  # name of the user, e.g. "Wei Xu"
            tweetUserAccount = tweet['user']['screen_name']  # name of the user account, e.g. "cocoweixu"

            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['text'])
            #print hashtags

            mywriter.writerows([(tweetId, tweetCreatedAt,tweetText,tweetUserId,tweetUserName,tweetUserAccount,hashtags)])
    except:
        # read in a line is not in JSON format (sometimes error occured)
        continue

    if tweet_count <= 0:
        break


csvfile.close()