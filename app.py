from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for development

@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML page

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    city_input = data.get("city", "")
    dropdown_choice = data.get("dropdown", "")
    
    response_data = {
        "percentage": 85,
        "checklist": ["item1", "item2", "item3", "item4"]
    }
    
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
