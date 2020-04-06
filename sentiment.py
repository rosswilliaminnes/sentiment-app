import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import secret

class TwitterApp():
    def __init__(self):
       
        consumer_key = secret.con_key
        consumer_secret = secret.con_secret
        access_token = secret.acctoken
        access_token_secret = secret.acctoken_secret

        self.auth = OAuthHandler(consumer_key, consumer_secret)  
        self.auth.set_access_token(access_token, access_token_secret) 
        self.api = tweepy.API(self.auth)

    def clean_tweet(self, tweet): 
        cleanedTweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", tweet).split())
        return cleanedTweet

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
            
        tweets = [] 

        fetched_tweets = self.api.search(q = query, count = count) # json format

        for tweet in fetched_tweets:

            parsed_tweet = {} 
            
            parsed_tweet['text'] = tweet.text               
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

            if tweet.retweet_count > 0: # do not duplicate retweets
                if parsed_tweet not in tweets: 
                    tweets.append(parsed_tweet) 
            else: 
                tweets.append(parsed_tweet) 
        
        return tweets # returns a dictionary in a list where the keys are 'text' and 'sentiment'

    def get_percentage(self,query,count=10):
        
        fetch = self.api.search(q= query, count = count) # note this line is used in the above method
        collect_sentiment = [self.get_tweet_sentiment(i.text) for i in fetch]

        positive_tweets = [i for i in collect_sentiment if i == 'positive']
        negative_tweets = [i for i in collect_sentiment if i == 'negative']
        neutral_tweets = [i for i in collect_sentiment if i == 'neutral']

        total_ptweets = len(positive_tweets)
        total_ntweets = len(negative_tweets)
        total_neutweets = len(neutral_tweets)
        total_alltweets = total_ptweets + total_ntweets + total_neutweets

        positive_percentage = f"Positive tweets percentage: {100*total_ptweets/total_alltweets} %"
        negative_percentage = "Negative tweets percentage: {} %".format(100*len(negative_tweets)/len(collect_sentiment))
        neutral_percentage = "Neutral tweets percentage: {} %".format(100*len(neutral_tweets)/len(collect_sentiment))

        return positive_percentage, negative_percentage, neutral_percentage


'''{
    searchTerm: '',
    overallProbability: {
        pos: 0,
        neg: 0,
        neut: 0
    },
    tweets: [
        {tweet:'', probability: {pos: 0, neg: 0, neut:0}}
    ]
}'''
        

        


if __name__ == "__main__":
    api = TwitterApp()
    #tweets = api.get_tweets(query = 'donald trump', count = 10)
    sentiment = api.get_percentage('donald trump',100)
    print(sentiment)