import praw
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ------------------------------------------
# 1. Clean text function
# ------------------------------------------
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

# ------------------------------------------
# 2. Sentiment analysis using VADER
# ------------------------------------------
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    return score['compound']

# ------------------------------------------
# 3. Reddit API Setup
# ------------------------------------------
client_id = '5AQBWn4UkacEZl_YG192yA'
client_secret = 'OWlyu31unR9o1JAipzpTS-Uslk7uKg'
user_agent = 'NewsVerifierBot'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# ------------------------------------------
# 4. Authenticated subreddits & query
# ------------------------------------------
authenticated_subs = [
    "news", "worldnews", "bbcnews", "reuters",
    "nytimes", "aljazeera", "CNN", "sports", "football", "politics"
]

query = "football player Diogo Jota Died?"

# ------------------------------------------
# 5. Search and analyze with new credibility logic
# ------------------------------------------
all_comments = []
verified_sources_count = 0
high_engagement_posts = 0

for sub in authenticated_subs:
    print(f"\n🔍 Searching '{query}' in r/{sub}...\n")
    subreddit = reddit.subreddit(sub)
    results = subreddit.search(query, sort='new', time_filter='month', limit=30)

    for post in results:
        if post.score < 5 or post.num_comments < 1:
            continue

        verified_sources_count += 1
        if post.ups > 50:
            high_engagement_posts += 1

        print("📰 Title           :", post.title)
        print("💬 Comments        :", post.num_comments)
        print("📍 Subreddit       :", sub)
        print("-" * 60)

        try:
            post.comments.replace_more(limit=0)
            comments = post.comments[:20]

            for i, comment in enumerate(comments):
                cleaned_comment = clean_text(comment.body)
                sentiment = analyze_sentiment(cleaned_comment)
                all_comments.append(cleaned_comment)

                print(f"🗨️  Comment {i+1}      :", comment.body)
                print("   Cleaned         :", cleaned_comment)
                print("   Sentiment Score :", round(sentiment, 2))
                print("-" * 40)

        except Exception as e:
            print("⚠️ Error reading comments:", e)

# ------------------------------------------
# 6. Final logic-based verdict
# ------------------------------------------
print("\n📊 Analyzing credibility signals...\n")

keywords_real = [
    "confirmed", "official", "reported", "identified", "statement", "verified", "announced",
    "declared", "according to", "evidence", "released", "published", "witnesses", "investigation",
    "recorded", "documented", "acknowledged", "testimony", "press release", "clarified", "authenticated",
    "authorities", "law enforcement", "approved", "confirmed by", "medical examiner", "autopsy"
]

keywords_fake = [
    "fake", "hoax", "misleading", "satire", "debunked", "rumor", "unverified", "conspiracy",
    "clickbait", "baseless", "false", "no evidence", "denied", "fabricated", "not true", "fake news",
    "mocked", "joke", "troll", "allegedly", "shocking but unconfirmed", "deepfake", "misstated",
    "manipulated", "exaggerated", "uncorroborated", "pseudoscience", "fraudulent"
]

real_flags = sum(any(k in c for k in keywords_real) for c in all_comments)
fake_flags = sum(any(k in c for k in keywords_fake) for c in all_comments)

if verified_sources_count >= 5 and high_engagement_posts >= 5 and fake_flags <= 5:
    verdict = "✅ FINAL VERDICT: Likely Real"
elif fake_flags >= 5 and fake_flags > real_flags:
    verdict = "❌ FINAL VERDICT: Possibly Fake"
else:
    verdict = "❓ FINAL VERDICT: Uncertain"


print(f"📌 Trusted Sources Mentioned: {verified_sources_count}")
print(f"📌 High Engagement Posts    : {high_engagement_posts}")
print(f"📌 Real-flagged Comments     : {real_flags}")
print(f"📌 Fake-flagged Comments     : {fake_flags}")
print(f"\n{verdict}\n")
