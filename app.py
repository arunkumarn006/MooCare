from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/data')
def data():
    data = get_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
