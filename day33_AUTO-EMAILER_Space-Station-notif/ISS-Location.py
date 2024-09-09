import requests
from datetime import datetime

MY_LAT = 51.507351
MY_LONG = -0.127758

# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# #generates the status code meaning associated with any result exceptions
# response.raise_for_status()
#
# #save the json data associated with the API call
# data = response.json()
# #you can pass in dictionary keys to request the specific values associated, just like how you would with a dictionary
# longitude = response.json()["iss_position"]["longitude"]
# latitude = response.json()["iss_position"]["latitude"]
#
# print(data)
# print(longitude)
# print(latitude)


#establish the parameters necesary for the API call
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted":0
}
# use a get() method to get the specific time of sunrise/sunset at our location
response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = data["results"]["sunset"].split("T")[1].split(":")[0]
#if: between sunset and sunrise; AND ISS within latitude range, look up
time_now = datetime.now()
print(time_now.hour)
print(sunrise)
print(sunset)
