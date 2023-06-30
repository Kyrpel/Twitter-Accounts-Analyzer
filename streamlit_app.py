import streamlit as st
import pandas as pd
from mongodb_handler import MongoDB
import matplotlib.pyplot as plt
from twitter_api import TwitterAPI


class StreamlitApp:
    def __init__(self, db_ip, db_port, db_name):
        self.db = MongoDB(db_ip, db_port, db_name)
        
    def len_database(self, collection_name):
            st.write(f"Number of documents in {collection_name} database: ", self.db.get_collection(collection_name).count_documents({}))

    # display a search bar for the user to enter a username to search 
    def display_search_bar(self):
        search_bar = st.sidebar.text_input("Enter a username to search")
        return search_bar

    def load_data(self, collection_name):
        collection = self.db.get_collection(collection_name)
        data = pd.DataFrame(list(collection.find()))
        return data

    def calculate_influence(self, followers_count, favorite_count):
        # This is a simple formula and may need to be adjusted based on your specific needs
        return followers_count + favorite_count

    def display_top_users(self, num_users):
        users = self.load_data("users_streamlit2")
        tweets = self.load_data("tweets_streamlit2")
        
        tweets['user_screen_name'] = tweets['user'].apply(lambda x: x['screen_name'])
        top_users = users.nlargest(num_users, "followers_count")

        for index, user in top_users.iterrows():
            user_tweets = tweets[tweets['user_screen_name'] == user['screen_name']]
            user['influence'] = self.calculate_influence(user['followers_count'],  user_tweets['favorite_count'].sum())
            
            # Create two columns
            col1, col2 = st.columns(2)
            
            # Display profile image in the left column
            col1.image(user['profile_image_url'], width=50)
            
            # Display user info in the right column
            col2.write(f"{user['name']} (@{user['screen_name']}) - {user['followers_count']} followers - Influence Score: {user['influence']}")
            
            top_tweets = user_tweets.nlargest(3, 'retweet_count')
            for i, tweet in top_tweets.iterrows():
                st.write(f"\t[Tweet](https://twitter.com/{tweet['user_screen_name']}/status/{tweet['id']}) - {tweet['retweet_count']} retweets")
            # break in between users
            st.write("")
            st.write("")

   
    # function that displays a wait loading icon and then displays the message "Fetching tweets..."
    def display_loading_message(self):
        return st.spinner("Fetching tweets from database...")

           

   
    def plot_data(self):
        users = self.load_data("users_streamlit2")

        # Plotting the top 20 users by followers count
        top_users = users.nlargest(20, "followers_count")
        plt.figure(figsize=(10,6))
        bars = plt.barh(top_users['screen_name'], top_users['followers_count'], color='skyblue')
        plt.xlabel("Followers Count")
        plt.title("Top 20 Users by Followers Count")
        plt.gca().invert_yaxis()
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, int(bar.get_width()), va='center')
        st.pyplot(plt)

        # Plotting the top 20 users by engagement
        top_users_by_engagement = users.nlargest(20, "engagement")
        plt.figure(figsize=(10,6))
        bars = plt.barh(top_users_by_engagement['screen_name'], top_users_by_engagement['engagement'], color='skyblue')
        plt.xlabel("Engagement")
        plt.title("Top 20 Users by Engagement")
        plt.gca().invert_yaxis()
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, int(bar.get_width()), va='center')
        st.pyplot(plt)

        # Plotting the top 20 users by tweet frequency
        top_users_by_frequency = users.nlargest(20, "average_tweets_per_day")
        plt.figure(figsize=(10,6))
        bars = plt.barh(top_users_by_frequency['screen_name'], top_users_by_frequency['average_tweets_per_day'], color='skyblue')
        plt.xlabel("Average Tweets Per Day")
        plt.title("Top 20 Users by Tweet Frequency")
        plt.gca().invert_yaxis()
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, int(bar.get_width()), va='center')
        st.pyplot(plt)

    def show_top_retweets_from_top_users(self):
        users = self.load_data("users_streamlit2")

        top_users = users.nlargest(10, "followers_count")

        top_retweets = self.TwitterAPI.fetch_top_retweets(10, top_users)        
    
    @st.cache
    def run(self):
            print("In run function")
            st.title("Cyprus Twitter Accounts Analyzer")
           
            # Display the number of users in the user database and in the tweets database
            self.len_database("users_streamlit2")
            self.len_database("tweets_streamlit2")

          
            # Button to show the results
            if st.button("Show Results"):
                self.display_top_users(10)
                self.plot_data()


                
if __name__ == "__main__":
    
    app = StreamlitApp('localhost', 27017, 'twitter')
    with st.spinner("Fetching tweets from database..."):
        app.run()