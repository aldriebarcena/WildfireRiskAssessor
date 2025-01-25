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
    
    # Example processing
    response_message = f"You entered '{city_input}' and selected '{dropdown_choice}'."
    return jsonify({"message": response_message})

if __name__ == "__main__":
    app.run(debug=True)
