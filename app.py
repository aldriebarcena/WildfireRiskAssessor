from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import google.generativeai as genai
import math
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Configure the Google generative AI API key
genai.configure(api_key="AIzaSyDhR97lvUuyyVmPBWyDJdtMoOfeG-OzZcs")

# Function to generate the checklist using the AI model
def generate_checklist(percentage, vegetation_type):
    # Generate content using the specified model
    model = genai.GenerativeModel("gemini-1.5-flash")
    checklist = model.generate_content(
        f"""
        Create a checklist of 6 for a person that lives in an area with {percentage}% wildfire risk and in a {vegetation_type}.
        Adjust the checklist according to risk + vegetation.
        Return the checklist that you end up making in the following format:

        {{
        "checklist": [
            "item1",
            "item2",
            "item3",
            ...
        ]
        }}

        DO NOT INCLUDE json and the ``` at the top.
        """
    )
    print(checklist.text)
    # Try to parse the JSON response
    try:
        checklist_data = json.loads(checklist.text)  # Parse the JSON response from the model
        
        # Return the parsed checklist
        return checklist_data.get("checklist", [])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # Handle the error and return an empty checklist if the JSON is invalid
        return [f"Error making checklist"]

def city_to_lat_long_API(city):
   # calls the city api call
   city_API_call_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid=4d0fee9539e02322b7161db27a699838"

   # this will have a json file 
   cityAPIresponse = requests.get(city_API_call_url)

   data = cityAPIresponse.json()

   cityLatitude = (data[0]['lat'])
   cityLongitude = (data[0]['lon'])
   

   return(cityLatitude, cityLongitude)


def scrapeWeather(lat_long_tuple):
   # lat and lon
   lat = lat_long_tuple[0]
   lon = lat_long_tuple[1]

   # change the variable inputting later to dynamic, problem is with the lat and lon variable api call inputting
   weather_API_call_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=4d0fee9539e02322b7161db27a699838'

   weatherAPIresponse = requests.get(weather_API_call_url)
   data = weatherAPIresponse.json()

   # take in weather, temperature, humidity, wind, and cloud cover

   weather = (data['weather'][0]['id']) # ID is a value

   # going to take in min and max because maybe this will help me with the calculations in the algorithm later
   temperature_min = ((data['main']['temp_min'])) # double
   temperature_max = ((data['main']['temp_max'])) # double
   temperature = ((data['main']['temp'])) # double

   wind = (data['wind']['speed']) # double
 
   humidity = (data['main']['humidity']) # double

   cloud = (data['clouds']['all']) #string??? turn into value

   # final tuple with all the data
   return(weather, temperature, temperature_min, temperature_max, wind, humidity, cloud)
   

# turn the vegetation into a hashmap, so when we cross reference it will be O(1) lookup
def vegetationMultiplier(vegetation):
   vegetationDict = {
      "coniferous" : 0.9,
      "deciduous" : 0.5,
      "shrubland" : 0.8,
      "grasslands" : 0.7,
      "savanna" : 0.6,
      "wetland" : 0.2,
      "agricultural" : 0.5,
      "urban" : 0.4,
      "barren" : 0.0,
      "mixed" : 0.6
   }

   # returns the vegetation multiplier
   return(vegetationDict[vegetation])

def IsaiahAlgorithm(city, vegetation):
    # checklist will just be an array of responses/things to do for the user
    city = city
    vegetation = vegetation

    # turns the city into a lat/lon
    lat_long_tuple = city_to_lat_long_API(city)

    # calls the scraper and returns a tuple of all the shit
    #(weather, temperature, temperature_min, temperature_max, wind, humidity, cloud)
    weather_data_tuple = scrapeWeather(lat_long_tuple)

    # we will assign them to separate variables so we can run calculations
    weather = weather_data_tuple[0]

    # if the weather is storming, raining, snowing, or something else, then we will return 0 because the wildfire likliehood is not that high
    if(weather >= 200 and weather <= 781):
        return 0.05

    # if the weather is clear, then we continue with the calculations

    # raw data
    temperature = weather_data_tuple[1]
    wind = weather_data_tuple[4]
    humidity = weather_data_tuple[5]
    cloud = weather_data_tuple[6]
    vegetation = vegetationMultiplier(vegetation)


    # weights
    temperature_weight = 0.3
    wind_weight = 0.25
    humidity_weight = 0.15
    cloud_weight = 0.05
    vegetation_weight = 0.25

    # calculating the individaul factors
    temperature_factor = (temperature - 250)/(350 - 250) 
    wind_factor = (wind/50)
    humidity_factor = humidity/100
    cloud_factor = cloud/100
    vegetation_factor = vegetation

    # the risk equation
    risk = (temperature_factor * temperature_weight) + (wind_factor * wind_weight) + (humidity_factor * humidity_weight) + (cloud_factor * cloud_weight) + (vegetation_factor * vegetation_weight)

    return(math.trunc(risk * 100))

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
    percentage = IsaiahAlgorithm(city_input, dropdown_choice)
    
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
