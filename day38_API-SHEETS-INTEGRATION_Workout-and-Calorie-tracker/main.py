import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv(f"{os.getcwd()}/.env")

GENDER = "Male"
WEIGHT_KG = 79.3787
HEIGHT_CM = 177.8
AGE = 32

NUTRITIONIX_APP_ID  = os.environ.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY =os.environ.get("NUTRITIONIX_API_KEY")
NLP_EXERCISE_ENDPOINT = os.environ.get("NLP_EXERCISE_ENDPOINT")
SHEETY_ADD_ENDPOINT = os.environ.get("SHEETY_ADD_ENDPOINT")
SHEETY_BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")

#------------------------------USE NUTRITIONIX TO CALCULATE DATA FROM NLP ---------------------------------- #
#nutritionix docs: https://docx.syndigo.com/developers/docs/natural-language-for-exercise
#Parse requests like "30 minutes yoga" and calculate the calories burned.

# SHEETY_PROJECT_NAME = "myWorkoutsNlpTracker"
# SHEETY_SPREADHSEET = "1aVMTzlDEKYq69eZiydtk60uD6sSBmg38ipsdQ868eNw"

exercise_input = input("Input the exercise you did: ")
#required headers
nutritionix_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY
}
#pass in parameters
nutritionix_data = {
    "query": exercise_input, #str
    "gender": GENDER,        #str
    "weight_kg": WEIGHT_KG,  #num
    "height_cm": HEIGHT_CM,  #num
    "age": AGE               #num
}

#request the post response to get the cals and data associated with the exercise done
response = requests.post(url= NLP_EXERCISE_ENDPOINT,headers=nutritionix_headers, json=nutritionix_data)
result = response.json()


#------------------------------USE THE SHEETY API TO ADD TO GOOGLE SHEETS ---------------------------------- #
# #use the Sheeety API to generate a new row of data into google sheet for each of the exercises that returned above
# https://docs.google.com/spreadsheets/d/1aVMTzlDEKYq69eZiydtk60uD6sSBmg38ipsdQ868eNw/edit?gid=0#gid=0

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
}

# print(result["exercises"])
today_date = datetime.now().strftime("%d%m%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheety_response = requests.post(
        url=SHEETY_ADD_ENDPOINT,
        json=sheet_inputs,
        headers=sheety_headers
    )
    print(sheety_response.text)

#------------------------------AUTHENTICATION ---------------------------------- #