from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Initialize a global variable to store the latest data
latest_data = {
    "heartRate": 0,
    "spo2": 0,
    "status": "Unknown",
    "timestamp": None
}

@app.route('/')
def index():
    return render_template('index.html', data=latest_data)

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    data = request.get_json()
    latest_data = {
        "heartRate": data.get('heartRate', 0),
        "spo2": data.get('spo2', 0),
        "status": data.get('status', 'Unknown'),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
