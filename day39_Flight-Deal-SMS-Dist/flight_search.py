import os
import requests
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(f"{os.getcwd()}/.env")

AMADEUS_FLIGHT_ENDPOINT = os.environ.get("AMADEUS_ENDPOINT")
AMADEUS_IATA_ENDPOINT = os.environ.get("AMADEUS_IATA_ENDPOINT")
AMADEUS_TOKEN_ENDPOINT = os.environ.get("AMADEUS_TOKEN_ENDPOINT")

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    #initialize the instance and set the apikey and apisecret
    def __init__(self):
        self._api_key = os.environ.get("AMADEUS_API_KEY"),
        self._api_secret = os.environ.get("AMADEUS_API_SECRET"),
        #get a new token every time the program is run; alt: reuse unexpired tokens as extension
        self._token = self._get_new_token()

    def _get_new_token(self):
        # Header with content type as per Amadeus documentation
        #makes a post request to the Amadeus token endpoint with the credentials (ApiKey ApiSecret);
        # updates the FlightSearch token
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body ={
            'grant_type': 'client_credentials',
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        #new bearer token is generated with the below
        response = requests.post(url=AMADEUS_TOKEN_ENDPOINT, headers=header, data=body)
        # New bearer token. Typically expires in 1799 seconds (30min)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']



    #Use flight search and Sheety to populate the worksheet with IATA codes for each city; use city code not airport
    def get_destination_code(self, city_name):
        # RETRIEVES THE IATA CODE FOR A CITY USING AMADEUS LOCATION API
        # parameters: City_name(str) : The name of the city for which to find the IATA code
        # returns: str: the IATA Code of the first matching city; else "N/A" if indexError; "Not Found" if KeyError
        #Sends a GET request to the IATA_ENDPOINT with a query that specifies the city name and other parameters to refine
        #then extracts IATA code from the JSON
        print(f"Using this token to get destination {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(
            url=AMADEUS_IATA_ENDPOINT,
            headers=headers,
            params=query
        )

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"
        return code

    def check_flights(self,origin_location_code, destination_location_code, from_time, to_time):
        #search for flight options between the two location IATA codes, on specified depart and return dates using API
        #params:
        # originLocationCode (str): IATA code of the departure city
        # destination_city_code (str): IATA code of the destination city
        # departure date
        # return date
        #returns dict or none. A dictionary containing the flight offer if the query is successful; None if  error
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            # APIKeyName : PythonCodeArg
            "originLocationCode":origin_location_code,
            "destinationLocationCode":destination_location_code,
            "departureDate":from_time.strftime("%Y-%m-%d"),
            "returnDate":to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode":"USD",
            "max": "10",
        }
        response = requests.get(
            url=AMADEUS_FLIGHT_ENDPOINT,
            headers=headers,
            params=query
        )

        #if error response; print help
        if response.status_code !=200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, reference the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None
        #else; return the response as json format
        return response.json()