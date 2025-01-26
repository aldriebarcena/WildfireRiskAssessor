from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import google.generativeai as genai
import math
import requests

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyDhR97lvUuyyVmPBWyDJdtMoOfeG-OzZcs")

def generate_checklist(percentage, vegetation_type):
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
    try:
        checklist_data = json.loads(checklist.text)
        return checklist_data.get("checklist", [])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return [f"Error making checklist"]

def city_to_lat_long_API(city):
   city_API_call_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid=4d0fee9539e02322b7161db27a699838"
   cityAPIresponse = requests.get(city_API_call_url)
   data = cityAPIresponse.json()
   cityLatitude = data[0]['lat']
   cityLongitude = data[0]['lon']
   return (cityLatitude, cityLongitude)

def scrapeWeather(lat_long_tuple):
   lat = lat_long_tuple[0]
   lon = lat_long_tuple[1]
   weather_API_call_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=4d0fee9539e02322b7161db27a699838'
   weatherAPIresponse = requests.get(weather_API_call_url)
   data = weatherAPIresponse.json()

   weather = data['weather'][0]['id']
   temperature_min = data['main']['temp_min']
   temperature_max = data['main']['temp_max']
   temperature = data['main']['temp']
   wind = data['wind']['speed']
   humidity = data['main']['humidity']
   cloud = data['clouds']['all']

   return (weather, temperature, temperature_min, temperature_max, wind, humidity, cloud)

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
   return vegetationDict[vegetation]

def IsaiahAlgorithm(city, vegetation):
    lat_long_tuple = city_to_lat_long_API(city)
    weather_data_tuple = scrapeWeather(lat_long_tuple)
    weather = weather_data_tuple[0]

    if weather >= 200 and weather <= 781:
        return 0.05

    temperature = weather_data_tuple[1]
    wind = weather_data_tuple[4]
    humidity = weather_data_tuple[5]
    cloud = weather_data_tuple[6]
    vegetation = vegetationMultiplier(vegetation)

    temperature_weight = 0.3
    wind_weight = 0.25
    humidity_weight = 0.15
    cloud_weight = 0.05
    vegetation_weight = 0.25

    temperature_factor = (temperature - 250) / (350 - 250)
    wind_factor = wind / 50
    humidity_factor = humidity / 100
    cloud_factor = cloud / 100
    vegetation_factor = vegetation

    risk = (temperature_factor * temperature_weight) + (wind_factor * wind_weight) + (humidity_factor * humidity_weight) + (cloud_factor * cloud_weight) + (vegetation_factor * vegetation_weight)

    return math.trunc(risk * 100)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    city_input = data.get("city", "")
    dropdown_choice = data.get("dropdown", "shrubland")
    percentage = IsaiahAlgorithm(city_input, dropdown_choice)
    checklist = generate_checklist(percentage, dropdown_choice)

    response_data = {
        "percentage": percentage,
        "checklist": checklist
    }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
