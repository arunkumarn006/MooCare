from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

sensor_data = {
    "ir": 0,
    "red": 0,
    "ecg": 0,
    "lat": None,
    "lon": None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def receive_data():
    global sensor_data
    sensor_data = request.json
    print('Received data:', sensor_data)
    return '', 200

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, ssl_context=('cert.pem', 'key.pem'))
