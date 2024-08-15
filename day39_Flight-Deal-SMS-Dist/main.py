import os

import notification_manager
from data_manager import DataManager
import time
from datetime import datetime, timedelta
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from pprint import pprint #json formatter

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

#--------------------------GET DATA FOR FLIGHT SEARCH------------------------------- #
#Populate the data from the gsheet into a variable called sheet_data
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
# print(sheet_data)
flight_search = FlightSearch()
ORIGIN_CITY_IATA = "LAX"


#--------------------------UPDATE AIRPORT CODES IN G SHEET------------------------------- #
# Check if the sheet_data contains any values for the "IATA Code" key; if not, the IATA Codes column is empty
#use the repsonse from the FlightSearch to update the sheet_data dictionary
#Pass each city name in the sheet_data one by one to the FlightSearch class. for now, respond with "TESTING"
for row in sheet_data:
    if sheet_data[0]["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        #time delay to avoid rate limit
        time.sleep(2)
pprint(f"sheet_data:\n{sheet_data}")

data_manager.destination_data = sheet_data #the sheet "prices" is the sheet_data
data_manager.update_destination_codes()


#--------------------------CHECK FOR THE CHEAPEST FLIGHTS NOW-6MO ------------------------------- #
#TODO: use flight search api to check cheapest flights from tomorrow-6months for all cities in sheet (10 max: rate limited)
    #Amadeus test api doesn't include all airports, you might not be able to retrieve prices for many routes flights
    #Nonstop flight prices from SFO to all destinations in the google sheet; 1 adult ticket
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    #for each "destination(row)" within the sheet data column 'city'
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        #Pass params from sheet to be used in API (required): originIATACode,DestinationIATAcode, Dept date,adults
        ORIGIN_CITY_IATA,   #CONSTANT DECLARED ABOVE
        destination["iataCode"],  #GATHERED FROM SHEET
        from_time = tomorrow,
        to_time =six_month_from_today
    )
    #take the data from the flights variable above in the for loop, push into the cheapest_flight method
    cheapest_flight = find_cheapest_flight(flights) #use data above iteratively in flight_data's class
    print(f"{destination['city']}: ${cheapest_flight.price}")
    time.sleep(2) #rate limiter mitigation


#---------------------RETRIEVE YOUR USER EMAIL ACCOUNTS--------------------------#
user_data = data_manager.get_user_emails()
customer_email_list = [row["What is your email address?"] for row in user_data]
# print(f"Your email list includdes {customer_email_list}")


#------------------------- SEND SMS AND EMAIL ALERT FOR NEW LOW PRICE ------------------------- #
# sms_manager = NotificationManager()
#if price is lower than lowest price in the sheet, send an SMS using twilio
if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
    if cheapest_flight.stops == 0:
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price found to {destination["city"]}!")

        notification_manager.send_sms(message_body=message)
        # Send emails to everyone on the list
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)