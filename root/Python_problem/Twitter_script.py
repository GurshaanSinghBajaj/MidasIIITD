import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
fetched_tweets_filename = "tweets_midas.json"
api = tweepy.API(auth)

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    
        print("...%s tweets downloaded so far" % (len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv	
    return alltweets

    #call to the function to get all the tweet information
    tweets = get_all_tweets('midasIIITD')

#importing other packages
import pandas as pd
import numpy as np


#function to extract information from the json object returned by the API
def tweets_to_data_frame(tweets):
    df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    df['id'] = np.array([tweet.id for tweet in tweets])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['date'] = np.array([tweet.created_at for tweet in tweets])
    df['source'] = np.array([tweet.source for tweet in tweets])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

    ###Tried extracting media information but it wasn't present in the json object
    ###only profile image url was present
    #df['Media'] = np.array([len(tweet.entities['media']) for tweet in tweets])
    return df


midas_df = tweets_to_data_frame(tweets)
print(midas_df)