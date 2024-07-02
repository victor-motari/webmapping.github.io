from flask import Flask, jsonify, render_template
import psycopg2

app = Flask(__name__)

# Database connection
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="web mapping db",
        user="postgres",
        password="1234567890",
        port="5432"
    )
except Exception as e:
    print(f"Error connecting to the database: {e}")
    conn = None

@app.route('/api/check_db')
def check_db():
    if conn is None:
        return "Database connection is not established.", 500
    try:
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.fetchone()
        cur.close()
        return "Database connection is successful!", 200
    except Exception as e:
        return str(e), 500

@app.route('/api/locations')
def get_locations():
    if conn is None:
        return jsonify({"error": "Database connection is not established."}), 500
    try:
        cur = conn.cursor()
        cur.execute('SELECT "national park", "northings", "eastings" FROM "coordinates of national parks"')
        rows = cur.fetchall()
        cur.close()
        locations = [{"name": row[0], "latitude": row[1], "longitude": row[2]} for row in rows]
        return jsonify(locations)
    except psycopg2.ProgrammingError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
