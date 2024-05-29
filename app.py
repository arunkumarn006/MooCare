from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Define the data model
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ir = db.Column(db.Float, nullable=False)
    red = db.Column(db.Float, nullable=False)
    ecg = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()

# Define the route for POSTing data
@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    ir = data['ir']
    red = data['red']
    ecg = data['ecg']
    lat = data['lat']
    lon = data['lon']
    new_entry = SensorData(ir=ir, red=red, ecg=ecg, lat=lat, lon=lon)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Data received'}), 201

# Define the route for GETting data
@app.route('/api/data', methods=['GET'])
def get_data():
    results = SensorData.query.all()
    data = [{
        'id': result.id,
        'ir': result.ir,
        'red': result.red,
        'ecg': result.ecg,
        'lat': result.lat,
        'lon': result.lon
    } for result in results]
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
