# Twitter Accounts Analyzer

This project is a Twitter data analysis tool that fetches tweets from Twitter using the Twitter API, saves the tweets and user data into a local MongoDB database, and then displays the results in a Streamlit app. The tool is specifically designed to analyze Twitter accounts in based on geoloaction.

## Project Structure

The project consists of several Python scripts:

- `twitter_api.py`: This script contains the `TwitterAPI` class, which is used to interact with the Twitter API. It fetches tweets based on a query and geolocation, and also fetches the top retweeted tweets of a user.

- `main.py`: This script is responsible for fetching the tweets and saving them to the MongoDB database. It also extracts and saves the users to the database.

- `streamlit_app.py`: This script is responsible for running the Streamlit app and displaying the results. It loads the data from the database and displays it in the app.

## How to Run

1. Run the `main.py` script to fetch and save the tweets and users.
```
python main.py
````

3. After the `main.py` script has finished executing, run the `streamlit_app.py` script to display the results.
   ```
   streamlit run streamlit_app.py
   ```

Please note that you need to run these commands in the directory where your scripts are located. Also, make sure that you have installed all the necessary packages and that your MongoDB server is running.

## Dependencies

This project requires the following Python packages:

- `tweepy`: To interact with the Twitter API.
- `pandas`: To manipulate and analyze the data.
- `streamlit`: To create the web app for displaying the results.
- `pymongo`: To interact with the MongoDB database.
- `matplotlib`: To create the plots for the data visualization.

You can install these packages with pip:
```
pip install tweepy pandas streamlit pymongo matplotlib
```

