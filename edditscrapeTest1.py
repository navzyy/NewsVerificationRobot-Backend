import praw
import re
import time
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
# 4. Track Start Time
# ------------------------------------------
start_time = time.time()

# ------------------------------------------
# 5. Query Reddit
# ------------------------------------------
query = "one person killed in india"
subreddit = reddit.subreddit("all")

results = subreddit.search(query, limit=3)

# ------------------------------------------
# 6. Process each post
# ------------------------------------------
postCount =0

for post in results:
    
    postCount += 1
    print("post no ",postCount)
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
        count  = 0
        for comment in post.comments[:100]:
            print("comments count = ",count)
            count+=1
            # Analyze first 5 top comments
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

# ------------------------------------------
# 7. Track End Time and Print Duration
# ------------------------------------------
end_time = time.time()
elapsed_time = end_time - start_time
print(f"⏱️ Total Processing Time: {round(elapsed_time, 2)} seconds")
