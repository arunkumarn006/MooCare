from flask import Flask, render_template

app = Flask(__name__)

# Sample cattle health data
cattle_data = [
    {"id": 1, "name": "Cow 10", "temperature": 38.5, "weight": 450, "status": "Healthy"},
    {"id": 2, "name": "Cow 2", "temperature": 39, "weight": 480, "status": "Sick"},
    {"id": 3, "name": "Cow 3", "temperature": 37.8, "weight": 420, "status": "Healthy"}
]

@app.route('/')
def index():
    return render_template('index.html', cattle_data=cattle_data)

if __name__ == '__main__':
    app.run(debug=True)
