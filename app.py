from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'sensor_data.db'

# Ensure the database is created
if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            irValue INTEGER,
            redValue INTEGER,
            ad8232Value INTEGER,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    irValue = data.get('irValue')
    redValue = data.get('redValue')
    ad8232Value = data.get('ad8232Value')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO sensor_data (irValue, redValue, ad8232Value, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    ''', (irValue, redValue, ad8232Value, latitude, longitude))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 201

@app.route('/view')
def view_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')
    data = c.fetchall()
    conn.close()
    
    return render_template('view.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
