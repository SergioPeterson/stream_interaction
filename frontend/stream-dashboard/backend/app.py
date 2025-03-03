from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from db import get_db_connection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Route to get all stream sessions
@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stream_sessions")
    sessions = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([{
        "session_id": s[0],
        "platform": s[1],
        "streamer_name": s[2],
        "start_time": s[3].isoformat()
    } for s in sessions])


# Route to get stats for all sessions
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stream_stats")
    stats = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "session_id": s[0],
        "followers_gained": s[1],
        "gifts": s[2],
        "comment_count": s[3],
        "top_commenter": s[4],
        "top_gifter": s[5]
    } for s in stats])


# Route to get viewer count for a session
@app.route('/api/viewers/<int:session_id>', methods=['GET'])
def get_viewers(session_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT minute, viewer_count FROM viewer_buckets WHERE session_id = %s", (session_id,))
    viewers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"minute": v[0], "viewer_count": v[1]} for v in viewers])


if __name__ == '__main__':
    app.run(debug=True)