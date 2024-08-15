import requests
import os
from twilio.rest import Client

OWM_ENDPOINT="https://api.openweathermap.org/data/2.5/forecast"
API_KEY = ""
#GET LAT LONG FROM Latlong.net for currently raining location
LAT = 38.7714
LONG =-90.3709
TWILIO_ACCOUNT_SID =""
TWILIO_AUTH_TOKEN=""
#TWILIO Number: +18335060881


weather_params= {
    "lat": LAT,
    "lon": LONG,
    "appid": API_KEY,
    "cnt": 4,
}

#MAKE AN API REQUEST TO FORECAST API 5day 3hr intvl weather call API:
#https://api.openweathermap.org/data/2.5/forecast?lat=33.72&lon=-116.22&appid=a18c00ccd8d3cf6b5468b332d245100d
response = requests.get(OWM_ENDPOINT,params=weather_params)
#PRINT HTTP STATUS CODE YOU GOT BACK
response.raise_for_status()
#PRINT THE RESPONSE TO THE CONSOLE
weather_data = response.json()
print(weather_data)
#LOCATE THE WEATHER ID AND DESCRIPTION FOR EACH FORECAST
will_rain = False
for hour_data in weather_data["list"]:
    #get the first itme in this list for the hour forecast, this will be the main weather condition
    data = hour_data["weather"][0]
    # print(data)
    weather_code = data["id"]
    weather_description = data["description"]
    # print(f"The forecast code is {weather_code}, so expect to see {weather_description}.")
    # codes less than 7##, bring umbrella
    if weather_code <700:
        will_rain = True

if will_rain:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella!",
        from_="+18335060881",
        to="+17608775865",
    )

    print(message.status)
