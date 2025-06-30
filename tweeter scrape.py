"""import tweepy
import re  

from clean_text import clean_text  # or paste the function in same file

# Your credentials
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAN3w2gEAAAAAIsAxLNl8JYKFylChTbk0InuPJAg%3DiT1hXQPLC476fy4TfyN4ZajfhGH44CXoTVoLfSaVyjTNZFxl3O'

# Create Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Example news query
query = "Eng vs Ind"

# Search recent tweets (max 20 for free access)
response = client.search_recent_tweets(query=query, max_results=2)

# Check if any tweets found
if response.data:
    for tweet in response.data:
        print("Tweet:", tweet.text)
else:
    print("No tweets found for this query.")
    


# Example:
cleaned_tweets = []
for tweet in response.data:
    original_text = tweet.text
    cleaned = clean_text(original_text)
    cleaned_tweets.append(cleaned)
"""
import tweepy
import re

# Define clean_text here or import from clean_text.py
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

# Your credentials
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAN3w2gEAAAAAIsAxLNl8JYKFylChTbk0InuPJAg%3DiT1hXQPLC476fy4TfyN4ZajfhGH44CXoTVoLfSaVyjTNZFxl3O'  # replace with valid key

# Create Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Example news query
query = "Air India plane crash survivor news"

# Search recent tweets (max 20)
response = client.search_recent_tweets(query=query, max_results=11)

# Collect and clean tweets
cleaned_tweets = []

if response.data:
    seen = set()
    print("\n Cleaned Tweets:\n")
    for tweet in response.data:
        text = tweet.text

        if text.startswith("RT"):  # Skip retweets
            continue

        cleaned = clean_text(text)

        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            print("Original:", text)
            print("Cleaned :", cleaned)
            print("-" * 50)
else:
    print(" No tweets found.")
