import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv(f"{os.getcwd()}/.env")
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.Authorization = os.environ.get("SHEETY_BEARER_TOKEN")
        #sheety endpoints as environment variables
        self.prices_endpoint = os.environ.get("SHEETY_PRICES_ENDPOINT")
        self.users_endpoint = os.environ.get("SHEETY_USERS_ENDPOINT")
        # Destination and user fields data start out empty
        self.destination_data = {}
        self.user_data = {}

    def get_destination_data(self):
        #get the data from the sheet
        response = requests.get(url=self.prices_endpoint)
        data = response.json()
        self.destination_data = data["prices"]
        #import pretty print and print the formatted data
        # pprint(data)
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data to update the Google Sheet with
    # the IATA codes. (Do this using code). HINT: Remember to check the checkbox to allow PUT requests in Sheety.
    def update_destination_codes(self):
        # for each city in the destination_data (data in the prices sheet), set the iataCode = city["iataCode"]
        # self.destination_data was updated in the main.py file when calling the FlightSearch.get_destination_code method
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.prices_endpoint}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def get_user_emails(self):
        response = requests.get(url=self.users_endpoint)
        data = response.json()
        self.user_data = data["users"]
        return self.user_data

# * Update the __init()__ method so that you retrieve all the environment variables in one place.
# This should include things like your SHEETY_USERNAME , your password, but also your endpoints.