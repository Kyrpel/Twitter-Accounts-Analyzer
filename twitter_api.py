import pandas as pd
import time
import tweepy

class TwitterAPI:
    def __init__(self, credentials):
        auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        self.api = tweepy.API(auth)

    def get_tweets(self, query, geocode, lang, num_tweets, count=100):
        print("Getting tweets...")
        tweets = []
        max_id = None

        while len(tweets) < num_tweets:
            try:
                batch = self.api.search_tweets(q=query, geocode=geocode, lang=lang, count=count, max_id=max_id)

                if not batch:
                    break  # no more tweets to fetch

                tweets.extend(batch[:min(len(batch), num_tweets - len(tweets))])
                max_id = tweets[-1].id - 1  # prepare the `max_id` for the next batch

            except tweepy.errors.TooManyRequests:
                # use tab and write a message to the user
                print("\tRate limit exceeded. Sleeping for 15 minutes.")                time.sleep(900)  # sleep for 15 minutes
                continue

        return tweets
    



    def fetch_top_retweets(self, user):
        # Fetch user's timeline in descending order of retweet count
        user_timeline = self.api.Cursor(id=user, tweet_mode='extended').items()

        # Sort tweets by retweet count in descending order
        sorted_tweets = sorted(user_timeline, key=lambda x: x.retweet_count, reverse=True)

        # Fetch the most retweeted tweets
        most_retweeted_tweets = sorted_tweets[:3] # fetch the top 3 most retweeted tweets
        return most_retweeted_tweets
