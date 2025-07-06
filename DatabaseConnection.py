import mysql.connector
from mysql.connector import Error
from datetime import datetime

class DatabaseConnection:
    def __init__(self, host='localhost', database='NewsVerificationRobot', user='root', password=''):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL database")
                self.cursor = self.connection.cursor()
        except Error as e:
            print("❌ Error connecting to MySQL:", e)
            self.connection = None

    def insert_query(self, query_text):
        sql = "INSERT INTO queries (query_text, created_at) VALUES (%s, %s)"
        self.cursor.execute(sql, (query_text, datetime.now()))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_post(self, query_id, title, subreddit, upvotes, comment_count):
        sql = """
        INSERT INTO posts (query_id, title, subreddit, upvotes, comment_count, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (query_id, title, subreddit, upvotes, comment_count, datetime.now()))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_comment(self, post_id, original_text, cleaned_text, sentiment_score, classification):
        sql = """
        INSERT INTO comments (post_id, original_text, cleaned_text, sentiment_score, classification, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            post_id, original_text, cleaned_text, sentiment_score, classification, datetime.now()))
        self.connection.commit()

    def insert_verdict(self, query_id, trusted_sources, high_engagement,
                       real_flags, fake_flags, supportive_total,
                       against_total, neutral_total, final_verdict):
        sql = """
        INSERT INTO verdicts (query_id, trusted_sources, high_engagement, real_flags, fake_flags,
                              supportive_total, against_total, neutral_total, final_verdict, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            query_id, trusted_sources, high_engagement, real_flags, fake_flags,
            supportive_total, against_total, neutral_total, final_verdict, datetime.now()))
        self.connection.commit()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🛑 MySQL connection closed.")
