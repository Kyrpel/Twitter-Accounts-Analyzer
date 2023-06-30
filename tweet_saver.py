import tweepy


class TweetSaver:

    def save_tweets_to_db(self, tweets, collection):
        print("In save tweets to db function")
        for tweet in tweets:
            tweet_dict = tweet._json
            collection.update_one(
                # avoid fetching duplicate tweets
                {"id": tweet_dict["id"]},
                {"$set": tweet_dict},
                upsert=True
            )
