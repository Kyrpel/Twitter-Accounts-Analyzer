from twitter_api import TwitterAPI
from mongodb_handler import MongoDB
from user_extractor import UserExtractor
from tweet_saver import TweetSaver
from streamlit_app import StreamlitApp
from streamlit_app import *
import pandas as pd
from tweet_extractor import TweetExtractor

if __name__ == "__main__":
    token = pd.read_csv('tokens.csv')
    credentials = {
        'consumer_key': token['consumer_key'].iloc[0],
        'consumer_secret': token['consumer_secret'].iloc[0],
        'access_token': token['access_token'].iloc[0],
        'access_token_secret': token['access_token_secret'].iloc[0]
    }

    api = TwitterAPI(credentials)
    db = MongoDB('localhost', 27017, 'twitter')
    extractor = UserExtractor()
    saver = TweetSaver()
    tweet_extractor = TweetExtractor()


    tweets = api.get_tweets("*", "35.1856,33.3823,100km", None, 1000)
    saver.save_tweets_to_db(tweets, db.get_collection("tweets_streamlit2"))

    # users = MongoDB('localhost', 27017, 'twitter').get_collection("users_streamlit2")

    
    # fetch the top retweets from api on top_users by num followers
    # top_retweets = tweet_extractor.extract_top_users_retweets(users)
    # saver.save_tweets_to_db(top_retweets, db.get_collection("tweets_streamlit2"))

    extractor.extract_and_save_users_to_db(tweets, db.get_collection("users_streamlit2"))

    # with app.display_loading_message():
    #     tweets = api.get_tweets("*", "35.1856,33.3823,100km", None, 50000)
    #     saver.save_tweets_to_db(tweets, db.get_collection("tweets_streamlit2"))
    #     extractor.extract_and_save_users_to_db(tweets, db.get_collection("users_streamlit2"))

