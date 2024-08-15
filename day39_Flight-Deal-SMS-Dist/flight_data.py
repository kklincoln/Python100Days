class FlightData:
    #This class is responsible for structuring the flight data.
    #initialize the flight data with the parameters that will be passed in from the flight_search API call in main.py
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price                              #cost of the flight
        self.origin_airport= origin_airport             #the IATA code for the flight's origin aiport
        self.destination_airport= destination_airport   #the IATA code for the flight's destination airport
        self.out_date= out_date                         #the departure date for the flight
        self.return_date= return_date                   #the return date for the flight

def find_cheapest_flight(data):
    """
    Parses flight data received from the Amadeus API to identify the cheapest flight option among
    multiple entries.
    Args:
        data (dict): The JSON data containing flight information returned by the API.
    Returns:
        FlightData: An instance of the FlightData class representing the cheapest flight found,
        or a FlightData instance where all fields are 'NA' if no valid flight data is available.
    This function initially checks if the data contains valid flight entries. If no valid data is found,
    it returns a FlightData object containing "N/A" for all fields. Otherwise, it starts by assuming the first
    flight in the list is the cheapest. It then iterates through all available flights in the data, updating
     the cheapest flight details whenever a lower-priced flight is encountered. The result is a populated
     FlightData object with the details of the most affordable flight.
    """

    # Handle empty data if no flight or Amadeus rate limit exceeded
    if data is None or not data['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    # Data from the first flight in the json
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight