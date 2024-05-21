
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

sensor_data = {}

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    global sensor_data
    sensor_data = request.json
    return 'Sensor data received', 200

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
