from datetime import datetime
import pytz

class UserExtractor:
    def extract_user_info_from_tweet(self, tweet):
        user_info = {
            'id': tweet.user.id,
            'id_str': tweet.user.id_str,
            'name': tweet.user.name,
            'screen_name': tweet.user.screen_name,
            'location': tweet.user.location,
            'description': tweet.user.description,
            'url': tweet.user.url,
            'followers_count': tweet.user.followers_count,
            'friends_count': tweet.user.friends_count,
            'listed_count': tweet.user.listed_count,
            'created_at': tweet.user.created_at,
            'favourites_count': tweet.user.favourites_count,
            'utc_offset': tweet.user.utc_offset,
            'time_zone': tweet.user.time_zone,
            'geo_enabled': tweet.user.geo_enabled,
            'verified': tweet.user.verified,
            'statuses_count': tweet.user.statuses_count,
            'lang': tweet.user.lang,
            'contributors_enabled': tweet.user.contributors_enabled,
            'is_translator': tweet.user.is_translator,
            'is_translation_enabled': tweet.user.is_translation_enabled,
            'profile_background_color': tweet.user.profile_background_color,
            'profile_background_image_url': tweet.user.profile_background_image_url,
            'profile_background_image_url_https': tweet.user.profile_background_image_url_https,
            'profile_background_tile': tweet.user.profile_background_tile,
            'profile_image_url': tweet.user.profile_image_url,
            'profile_image_url_https': tweet.user.profile_image_url_https,
            'profile_link_color': tweet.user.profile_link_color,
            'profile_sidebar_border_color': tweet.user.profile_sidebar_border_color,
            'profile_sidebar_fill_color': tweet.user.profile_sidebar_fill_color,
            'profile_text_color': tweet.user.profile_text_color,
            'profile_use_background_image': tweet.user.profile_use_background_image,
            'has_extended_profile': tweet.user.has_extended_profile,
            'default_profile': tweet.user.default_profile,
            'default_profile_image': tweet.user.default_profile_image,
            'following': tweet.user.following,
            'follow_request_sent': tweet.user.follow_request_sent,
            'notifications': tweet.user.notifications,
            'translator_type': tweet.user.translator_type,
            'withheld_in_countries': tweet.user.withheld_in_countries,
            'average_tweets_per_day': self.calculate_tweet_frequency(tweet.user),  # Tweet frequency
            'engagement': self.calculate_engagement(tweet)  # Engagement
        }
        return user_info

    # def calculate_tweet_frequency(self, user):
    #     account_age_days = (datetime.datetime.now() - user.created_at).days
    #     if account_age_days > 0:
    #         return user.statuses_count / account_age_days
    #     else:
    #         return user.statuses_count
        
    def calculate_tweet_frequency(self, user):
        now = datetime.now(pytz.UTC)  # make 'now' offset-aware by setting it to UTC
        account_age_days = (now - user.created_at).days

        if account_age_days > 0:
            return user.statuses_count / account_age_days
        else:
            # the total numbers of tweets includes retweets have ever made
            return user.statuses_count
        
    # calculate the avarage retweet of all tweets of the user in a single day
    

    def calculate_engagement(self, tweet):
        tweet_frequency = self.calculate_tweet_frequency(tweet.user)
        return (tweet.favorite_count + tweet_frequency) / tweet.user.followers_count if tweet.user.followers_count > 0 else 0

    def save_single_user_to_db(self, user, collection):
        if collection.find_one({'id': user['id']}) is None:
            collection.insert_one(user)

    def extract_and_save_users_to_db(self, tweets, collection):
        print("In extract and save users to db function")
        for tweet in tweets:
            user_info = self.extract_user_info_from_tweet(tweet)
            self.save_single_user_to_db(user_info, collection)



