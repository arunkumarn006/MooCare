from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER PRIMARY KEY AUTOINCREMENT, ad8232 FLOAT, gps_lat FLOAT, gps_long FLOAT)''')
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ad8232 = request.json.get('ad8232')
        gps_lat = request.json.get('gps_lat')
        gps_long = request.json.get('gps_long')
        
        # Store data in database
        conn = sqlite3.connect('sensor_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO sensor_data (ad8232, gps_lat, gps_long) VALUES (?, ?, ?)", (ad8232, gps_lat, gps_long))
        conn.commit()
        conn.close()
        
        return 'Data received successfully', 200
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
