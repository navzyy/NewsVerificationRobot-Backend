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
# 2. Sentiment analysis setup
# ------------------------------------------
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    return score['compound']

# ------------------------------------------
# 3. Reddit API Setup (AUTHENTICATION)
# ------------------------------------------
reddit = praw.Reddit(
   client_id='5AQBWn4UkacEZl_YG192yA',
   client_secret='OWlyu31unR9o1JAipzpTS-Uslk7uKg',
   user_agent='NewsVerifierBot'
)

# ------------------------------------------
# 4. Subreddits and query
# ------------------------------------------
trusted_subs = [
    "news", "worldnews", "bbcnews", "reuters", "nytimes", "aljazeera", "CNN", "sports"
]

query = "Texas Flood"

# ------------------------------------------
# 5. Keywords for real/fake news detection
# ------------------------------------------
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

# ------------------------------------------
# 6. Search and process posts
# ------------------------------------------
all_comments = []
supportive_comments = []
against_comments = []

verified_sources_count = 0
high_engagement_posts = 0
supportive_total = 0
against_total = 0
neutral_total = 0

print(f"\n🔍 Searching '{query}' in trusted subreddits...\n")

for sub in trusted_subs:
    subreddit = reddit.subreddit(sub)
    results = subreddit.search(query, sort='new', time_filter='month', limit=10)

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
            comments = post.comments[:10]

            for i, comment in enumerate(comments):
                cleaned = clean_text(comment.body)
                sentiment = analyze_sentiment(cleaned)
                all_comments.append(cleaned)

                # Classification
                if any(k in cleaned for k in ["true", "confirmed", "i saw", "real", "this happened", "rip", "sad", "terrible",
                                             "tragedy", "devastating", "so sorry", "my condolences", "can't believe", "heartbreaking",
                                             "rest in peace", "legit", "genuine", "authentic", "witnessed", "heard", "verified", "happened"]):
                    supportive_total += 1
                    supportive_comments.append(comment.body)
                elif any(k in cleaned for k in ["fake", "fake news", "this is fake", "this is false", "clickbait", "fabricated", "not true", "hoax", "lie", "conspiracy" "misleading", "debunked",
                                                "satire", "no evidence", "rumor", "photoshop", "edited", "unconfirmed", "fabricated",
                                                "exaggerated", "scam", "bot posted", "ai generated", "manipulated", "nonsense"]):
                    against_total += 1
                    against_comments.append(comment.body)
                else:
                    if sentiment >= 0.1:
                        supportive_total += 0.5
                        supportive_comments.append(comment.body)
                    elif sentiment <= -0.2:
                        against_total += 0.5
                        against_comments.append(comment.body)
                    else:
                        neutral_total += 1

                print(f"🗨️  Comment {i+1}      :", comment.body)
                print("   Cleaned         :", cleaned)
                print("   Sentiment Score :", round(sentiment, 2))
                print("-" * 40)

        except Exception as e:
            print("⚠️ Error reading comments:", e)

# ------------------------------------------
# 7. Final Verdict Logic
# ------------------------------------------
real_flags = sum(any(k in c for k in keywords_real) for c in all_comments)
fake_flags = sum(any(k in c for k in keywords_fake) for c in all_comments)

print("\n📊 Analyzing credibility signals...\n")
print(f"📌 Trusted Sources Mentioned : {verified_sources_count}")
print(f"📌 High Engagement Posts     : {high_engagement_posts}")
print(f"📌 Real-flagged Comments     : {real_flags}")
print(f"📌 Fake-flagged Comments     : {fake_flags}")
print(f"📌 Supportive Comments Count : {supportive_total}")
print(f"📌 Against Comments Count    : {against_total}")
print(f"📌 Neutral Comments Count    : {neutral_total}")

# Verdict logic
if supportive_total >= against_total and real_flags >= fake_flags and verified_sources_count >= 2:
    verdict = "✅ FINAL VERDICT: Likely Real"
elif against_total > supportive_total and fake_flags >= 4:
    verdict = "❌ FINAL VERDICT: Possibly Fake"
else:
    verdict = "❓ FINAL VERDICT: Uncertain"

print(f"\n{verdict}\n")

# ------------------------------------------
# 8. Show flagged comments
# ------------------------------------------
print("🟢 Supportive Comments:\n")
for com in supportive_comments:
    print(" -", com.strip(), "\n")

print("\n🔴 Against Comments:\n")
for com in against_comments:
    print(" -", com.strip(), "\n")
