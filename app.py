from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Configure the Google generative AI API key
genai.configure(api_key="AIzaSyDhR97lvUuyyVmPBWyDJdtMoOfeG-OzZcs")

# Function to generate the checklist using the AI model
def generate_checklist(percentage, vegetation_type):
    # Generate content using the specified model
    model = genai.GenerativeModel("gemini-1.5-flash")
    checklist = model.generate_content(f'''
    Create a short checklist for a person that lives in an area with {percentage}% wildfire risk and in a {vegetation_type}. Return the checklist in the following format:

    {{
      "checklist": [
        "item1",
        "item2",
        "item3",
        ...
      ]
    }}
    DO NOT INCLUDE json and the ``` at the top
    ''')

    # Try to parse the JSON response
    try:
        checklist_data = json.loads(checklist.text)  # Parse the JSON response from the model
        
        # Return the parsed checklist
        return checklist_data.get("checklist", [])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # Handle the error and return an empty checklist if the JSON is invalid
        return []

# Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML page

# Define the route for processing requests
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    city_input = data.get("city", "")
    dropdown_choice = data.get("dropdown", "shrubland")  # Default to "shrubland" if not provided
    percentage = 85
    
    # Call the generate_checklist function to get the checklist data
    checklist = generate_checklist(percentage, dropdown_choice)

    # Prepare the final response data
    response_data = {
        "percentage": percentage,  # Use the provided percentage
        "checklist": checklist  # Add the generated checklist
    }

    # Return the response data as JSON
    return jsonify(response_data)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
