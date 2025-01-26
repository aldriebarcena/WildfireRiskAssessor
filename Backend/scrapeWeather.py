import requests 
import json

city = "Sacramento"
vegetation = "Forest"

# just make it static for now

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
      "Forest (Confierous)" : 0.9,
      "Forest (Deciduous)" : 0.5,
      "Shrubland (Chaparral)" : 0.8,
      "Grasslands" : 0.7,
      "Savanna" : 0.6,
      "Wetland Vegetation" : 0.2,
      "Agricultural Land" : 0.5,
      "Urban Landscaping" : 0.4,
      "Barren Land (No Vegetation)" : 0.0,
      "Mixed Vegetation" : 0.6
   }

   # returns the vegetation multiplier
   return(vegetationDict[vegetation])


'''
Vegetation:

Forest (Coniferous): Pine trees, fir trees, spruce—highly flammable when dry.
Forest (Deciduous): Oak, maple, and other broadleaf trees—generally less flammable than conifers but still a risk when dry.
Shrubland (Chaparral): Dense, drought-resistant shrubs like scrub oak, sagebrush—highly flammable.
Grasslands: Open areas with grasses—can ignite easily during dry conditions.
Savanna: A mix of grasslands and scattered trees—moderate fire risk depending on dryness.
Wetland Vegetation: Marshes and wetlands with grasses, reeds, and other water-dependent plants—lower fire risk, but risk can rise in drought conditions.
Agricultural Land: Crops like wheat, corn, and other crops—depends on crop moisture content and surrounding conditions.
Urban Landscaping: Gardens, lawns, and ornamental plants—can contribute to fire spread, especially if dry.
Barren Land (No Vegetation): Areas without vegetation, such as deserts or bare earth—no fire risk.
Mixed Vegetation: Areas with a combination of forest, grass, and shrub types—risk can vary depending on the mix.

we will have each vegetation equal to a multiplier value

when we are running the calculations we will have the weather risk calculation from the data we scraped, then multiply that by the multiplier to get a final value
this final value is the final risk. 

make the checklist

return a json file with 
- the final value
- checklist (array of shit to do)
'''