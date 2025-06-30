"""import praw

# Your credentials
client_id = '5AQBWn4UkacEZl_YG192yA'         # YOUR client_id
client_secret = 'OWlyu31unR9o1JAipzpTS-Uslk7uKg'  # YOUR client_secret
user_agent = 'NewsVerifierBot'

# Create Reddit client
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Search news query (example)
query = "BAN vs SL"
subreddit = reddit.subreddit("all")

# Search Reddit posts
results = subreddit.search(query, limit=5)

# Process results
for post in results:
    print("Title:", post.title)
    print("Upvotes:", post.score)
    print("Comments:", post.num_comments)
    print("Posted by:", post.author)
    print("-" * 40)"""
    
import praw
import re
from textblob import TextBlob

# ------------------------------------------
# 1. Clean function
# ------------------------------------------
def clean_text(text):
    text = re.sub(r"http\S+", "", text)        # Remove links
    text = re.sub(r"@\w+", "", text)           # Remove mentions
    text = re.sub(r"#\w+", "", text)           # Remove hashtags
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove emojis / Unicode
    text = re.sub(r"[^\w\s]", "", text)        # Remove punctuation
    return text.lower().strip()

# ------------------------------------------
# 2. Sentiment function
# ------------------------------------------
def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity  # value: -1.0 (negative) to +1.0 (positive)

# ------------------------------------------

# 3. Reddit API Setup
# ------------------------------------------
client_id = '5AQBWn4UkacEZl_YG192yA'         # YOUR client_id
client_secret = 'OWlyu31unR9o1JAipzpTS-Uslk7uKg'  # YOUR client_secret
user_agent = 'NewsVerifierBot'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# ------------------------------------------
# 3. Query Reddit
# ------------------------------------------
query = "Air India crash survivor"
subreddit = reddit.subreddit("all")

results = subreddit.search(query, limit=5)

# ------------------------------------------
# 4. Process and clean each post
# ------------------------------------------
for post in results:
    original_title = post.title
    cleaned_title = clean_text(original_title)
    sentiment = analyze_sentiment(cleaned_title)

    print("Original Title:", original_title)
    print("Cleaned Title :", cleaned_title)
    print("Sentiment Score:", round(sentiment, 2))
    print("Upvotes       :", post.score)
    print("Comments      :", post.num_comments)
    print("Posted by     :", post.author)
    print("-" * 50)

try:
        post.comments.replace_more(limit=0)
        comment_sentiments = []

        for comment in post.comments[:5]:  # Analyze first 5 top comments
            cleaned_comment = clean_text(comment.body)
            score = analyze_sentiment(cleaned_comment)
            comment_sentiments.append(score)

            print("🗨️  Comment        :", comment.body)
            print("   Cleaned         :", cleaned_comment)
            print("   Sentiment Score :", round(score, 2))
            print("-" * 40)

        if comment_sentiments:
            avg_comment_sentiment = sum(comment_sentiments) / len(comment_sentiments)
            print(f"📘 Avg Comment Sentiment: {round(avg_comment_sentiment, 2)}")
        else:
            print("📘 No valid comments to analyze.")

except Exception as e:
        print("⚠️ Error reading comments:", e)

print("=" * 60)