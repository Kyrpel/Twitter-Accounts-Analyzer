    
from twitter_api import TwitterAPI
# import mongodb


class TweetExtractor:
    def __init__(self):
        pass
# extract top 10 users RTt
    def extract_top_users_retweets(self, user):
        # users = []
        top_retweets = TwitterAPI.fetch_top_retweets(user['screen_name'])
        return top_retweets
