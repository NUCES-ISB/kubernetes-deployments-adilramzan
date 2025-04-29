"""
Flask application for Kubernetes demo with PostgreSQL integration.
Provides endpoints for health checks, database testing, and message management.
"""
import os
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "flaskapp")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def get_db_connection():
    """Create a database connection"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    return conn

@app.route('/')
def index():
    """Main endpoint that returns a welcome message"""
    return jsonify({
        "message": "Welcome to Flask Kubernetes Demo",
        "status": "active"
    })

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        "status": "healthy"
    })

@app.route('/db-test')
def db_test():
    """Test database connection"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Try to create a table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Get count of records
        cur.execute("SELECT COUNT(*) as count FROM messages")
        count = cur.fetchone()['count']

        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "database_connection": "successful",
            "message_count": count
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "database_connection": "failed",
            "error": str(e)
        }), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get all messages from the database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
        messages = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "count": len(messages),
            "messages": messages
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/messages', methods=['POST'])
def create_message():
    """Create a new message"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "status": "error",
                "error": "Message field is required"
            }), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "INSERT INTO messages (message) VALUES (%s) RETURNING id, message, created_at",
            (data['message'],)
        )
        new_message = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Message created successfully",
            "data": new_message
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
