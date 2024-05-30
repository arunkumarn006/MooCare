from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cow_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for the health data
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heart_rate = db.Column(db.Float, nullable=False)
    spo2 = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HealthData {self.heart_rate} {self.spo2} {self.status}>'

# Create the database and the table
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    latest_data = HealthData.query.order_by(HealthData.timestamp.desc()).first()
    if latest_data:
        data = {
            "heartRate": latest_data.heart_rate,
            "spo2": latest_data.spo2,
            "status": latest_data.status,
            "timestamp": latest_data.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        data = {
            "heartRate": 0,
            "spo2": 0,
            "status": "Unknown",
            "timestamp": "N/A"
        }
    return render_template('index.html', data=data)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    heart_rate = data.get('heartRate', 0)
    spo2 = data.get('spo2', 0)
    status = data.get('status', 'Unknown')

    # Create a new health data record
    new_data = HealthData(heart_rate=heart_rate, spo2=spo2, status=status)
    db.session.add(new_data)
    db.session.commit()

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
