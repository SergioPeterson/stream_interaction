import psycopg2
import psycopg2.extras
import json
import os
from collections import defaultdict
from datetime import datetime

class Analytics:
    def __init__(self, platform):
        """Initialize PostgreSQL connection and create necessary tables."""
        self.platform = platform
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "streaming_analytics"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Cache for aggregated data
        self.follower_count = defaultdict(int)
        self.gift_summary = defaultdict(lambda: defaultdict(int))
        self.gift_points = defaultdict(int)  # New: Store gift points
        self.comment_count = defaultdict(int)
        self.commenters = defaultdict(lambda: defaultdict(int))  # {session_id: {user: comment_count}}
        self.viewer_buckets = defaultdict(list)  # {session_id: [(minute, count), ...]}
        self.start_times = {}  # {session_id: start_time}
    
    def create_tables(self):
        """Create necessary tables if they do not exist."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS stream_sessions (
                session_id SERIAL PRIMARY KEY,
                platform VARCHAR(50),
                streamer_name VARCHAR(100),
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                run_time INTERVAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS stream_stats (
                session_id INT REFERENCES stream_sessions(session_id),
                followers_gained INT DEFAULT 0,
                gifts JSONB DEFAULT '{}'::jsonb,
                gift_points INT DEFAULT 0,
                comment_count INT DEFAULT 0,
                top_commenter VARCHAR(100) DEFAULT NULL,
                top_gifter VARCHAR(100) DEFAULT NULL,
                PRIMARY KEY (session_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS viewer_buckets (
                id SERIAL PRIMARY KEY,
                session_id INT REFERENCES stream_sessions(session_id),
                minute INT,
                viewer_count INT
            )
            """
        ]
        for query in queries:
            self.cursor.execute(query)
        self.conn.commit()

    def start_stream_session(self, streamer_name):
        """Create a new stream session entry with formatted start time."""
        formatted_start_time = datetime.now().strftime('%m/%d/%Y %H:%M')

        query = """
        INSERT INTO stream_sessions (platform, streamer_name, start_time) 
        VALUES (%s, %s, %s) RETURNING session_id;
        """
        self.cursor.execute(query, (self.platform, streamer_name, formatted_start_time))
        session_id = self.cursor.fetchone()[0]

        # Initialize stats entry
        query = """INSERT INTO stream_stats (session_id) VALUES (%s)"""
        self.cursor.execute(query, (session_id,))
        self.conn.commit()

        # Store start time
        self.start_times[session_id] = datetime.now()
        return session_id

    # ===========================
    # Accumulate Data
    # ===========================

    def increment_followers(self, session_id):
        """Increase follower count for the session."""
        self.follower_count[session_id] += 1

    def aggregate_gift(self, session_id, gift_name, count, sender, gift_value):
        """Accumulate total count for each gift type, track sender, and add gift points."""
        self.gift_summary[session_id][gift_name] += count
        self.gift_summary[session_id][sender] += count  # Track sender for top gifter
        self.gift_points[session_id] += gift_value  # Track gift points

    def save_comment(self, session_id, user_id):
        """Count total comments and track top commenter."""
        self.comment_count[session_id] += 1
        self.commenters[session_id][user_id] += 1  # Track comment frequency per user

    def save_viewer_count(self, session_id, minute, viewer_count):
        """Store viewer count for each minute"""
        query = """
        INSERT INTO viewer_buckets (session_id, minute, viewer_count) 
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (session_id, minute, viewer_count))
        self.conn.commit()

    # ===========================
    # Flush Aggregated Data
    # ===========================

    def flush_summary_to_db(self):
        """Save aggregated data (followers, gifts, comments, top commenter, top gifter, gift points, and runtime) to PostgreSQL."""
        for session_id in self.follower_count:
            # Determine top commenter
            if self.commenters[session_id]:
                top_commenter = max(self.commenters[session_id], key=self.commenters[session_id].get)
            else:
                top_commenter = None

            # Determine top gifter
            gift_senders = {sender: count for sender, count in self.gift_summary[session_id].items() if sender not in self.gift_summary[session_id]}
            if gift_senders:
                top_gifter = max(gift_senders, key=gift_senders.get)
            else:
                top_gifter = None

            # Calculate formatted end time and runtime
            formatted_end_time = datetime.now().strftime('%m/%d/%Y %H:%M')
            if session_id in self.start_times:
                run_time = datetime.now() - self.start_times[session_id]
            else:
                run_time = None  # Fallback if no start time is found

            # Update stream_stats table
            query = """
            UPDATE stream_stats 
            SET followers_gained = %s, gifts = %s::jsonb, gift_points = %s, comment_count = %s, 
                top_commenter = %s, top_gifter = %s
            WHERE session_id = %s
            """
            self.cursor.execute(query, (
                self.follower_count[session_id],
                json.dumps(self.gift_summary[session_id]),
                self.gift_points[session_id],
                self.comment_count[session_id],
                top_commenter,
                top_gifter,
                session_id
            ))

            # **NEW**: Update stream_sessions table with end time and runtime
            query = """
            UPDATE stream_sessions 
            SET end_time = %s, run_time = %s
            WHERE session_id = %s
            """
            self.cursor.execute(query, (formatted_end_time, run_time, session_id))

        self.conn.commit()

        # Reset cache
        self.follower_count.clear()
        self.gift_summary.clear()
        self.gift_points.clear()
        self.comment_count.clear()
        self.commenters.clear()
        self.start_times.clear()


    def close(self):
        """Flush all accumulated data and close the connection."""
        self.flush_summary_to_db()
        self.cursor.close()
        self.conn.close()