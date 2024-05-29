from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Setup SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ir = db.Column(db.Integer, nullable=False)
    red = db.Column(db.Integer, nullable=False)
    ecg = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    sensor_data = SensorData(
        ir=data['ir'],
        red=data['red'],
        ecg=data['ecg'],
        lat=data.get('lat'),
        lon=data.get('lon')
    )
    db.session.add(sensor_data)
    db.session.commit()
    return '', 200

@app.route('/api/data', methods=['GET'])
def get_data():
    sensor_data = SensorData.query.order_by(SensorData.id.desc()).first()
    if sensor_data:
        return jsonify({
            'ir': sensor_data.ir,
            'red': sensor_data.red,
            'ecg': sensor_data.ecg,
            'lat': sensor_data.lat,
            'lon': sensor_data.lon
        })
    else:
        return jsonify({}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
