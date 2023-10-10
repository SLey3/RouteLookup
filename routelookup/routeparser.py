# Imports
from FlightRadar24 import FlightRadar24API
from FlightRadar24.errors import CloudflareError
from pathlib import Path
from Config import config
from typing import Dict
from time import sleep
import os

# initialize fr_api and FILE_DIR
fr_api = FlightRadar24API(config.FLIGHTRADAR_USERNAME, config.FLIGHTRADAR_PASSWORD)
config.FLIGHTRADAR_API = fr_api
FILE_DIR = Path(__file__).resolve().parent / "data" / "data.txt"
status = []
cleaned_flights = []
total_flights = []

# classes

class Airline:
    def __init__(self, airline: Dict):
        self.name = airline['Name']
        self.icao = airline['ICAO']
        self.code = airline['Code']
        self.actype = self.callsign = \
        self.origin = self.destination = None
    
    def set_parameters(self, actype: str, callsign: str, origin: str, destination: str):
        self.actype = actype
        self.callsign = callsign
        self.origin = origin
        self.destination = destination


class RouteList:
    def __init__(self):
        self.routes = []

    def add_routes(self, airline: Airline):
        self.routes.append(airline)

    def get(self, name):
        if self.routes != []:
            sample = self.routes[0]
        else:
            return None
        return sample.__getattribute__(name)

    def clear(self):
        self.routes.clear()

    def __iter__(self):
        yield from self.routes

# only for use on app.py
def fr_api_logout():
    fr_api.logout()

# helper functions
def get_airline(icao):
    """
    get airline information based from ICAO code
    """
    airline = None

    for airline_dict in fr_api.get_airlines():
        if airline_dict["ICAO"] == icao:
            airline = airline_dict
            break
    return airline

def get_flight_variables(flight):
    for line in flight:
        line = line.split(": ")
        if line[0] == "A/C TYPE":
            actype = line[1]
        elif line[0] == "CALLSIGN":
            callsign = line[1]
        elif line[0] == "ORIGIN":
            origin = line[1]
        else:
            destination = line[1]
    return (actype, callsign, origin, destination,)


def _get_origin_airport(flight):
    try:
        origin = fr_api.get_airport(flight.origin_airport_iata)
    except CloudflareError:
        sleep(10) # this prevents the CloudflareError through delaying time between
                  # requests sent to FlightRadar
        origin = fr_api.get_airport(flight.origin_airport_iata)
    except TypeError:
        return f"{flight.origin_airport_iata}"
    
    return origin.icao

def _get_destination_airport(flight):
    try:
        dest = fr_api.get_airport(flight.destination_airport_iata)
    except CloudflareError:
        sleep(10) # this prevents the CloudflareError through delaying time between
                  # requests sent to FlightRadar
        dest = fr_api.get_airport(flight.destination_airport_iata)
    except TypeError:
        return f"{flight.destination_airport_iata}"
    
    return dest.icao


def init_file(icao):
    """
    generates data.txt if it isn't already created and init essential items
    """
    global total_flights, cleaned_flights

    flights = fr_api.get_flights(icao)

    cleaned_flights.append(clean_flights(flights))
    total_flights.clear()
    total_flights.append(len(cleaned_flights[0]) + 1)


    config.AIRLINE_FLIGHTS_LEN = total_flights[0]

    if not os.path.exists(FILE_DIR):
        open(FILE_DIR, 'w').close()

def refresh():
    """
    In the event that a new airline is set (e.g. AAL --> DAL), this will delete all text
    and regenerate the routes
    """ 
    config.CURRENT_AIRLINE = ""
    config.AIRLINE_FLIGHTS_LEN = ""

    if isinstance(config.AIRLINE_LIST, RouteList):
        config.AIRLINE_LIST.clear()
        config.AIRLINE_LIST = ""

def reset_contents(all=False):
    """
    reset data.txt to default state:
    * All Route information deleted
    * "AIRLINE" info reset to "None"
    """
    with open(FILE_DIR, 'w') as f:
        f.seek(0)
        f.truncate()
        if not all:
            f.write("AIRLINE: None")


def clean_flights(flights: list):
    for flight in flights[:]:
        if (flight.destination_airport_iata == 'N/A' or 
            flight.origin_airport_iata == 'N/A'):
            flights.remove(flight)
    return flights


def generate_routes(icao):
    """
    Generate airline routes and insert them into data.txt
    """
    global cleaned_flights, status

    airline = get_airline(icao)

    if isinstance(airline, dict): # basically if airline is not None
        flights = cleaned_flights.pop(0)

        with open(FILE_DIR, 'w') as file:
            reset_contents() # wipe data.txt clean before processing

            config.CURRENT_AIRLINE = airline

            status.append(1)
            
            file.write(f"AIRLINE: {airline['ICAO']}\n")

            for flight in flights:
                aircraft_type = flight.aircraft_code
                callsign = flight.callsign
                origin_icao = _get_origin_airport(flight)
                destination_icao = _get_destination_airport(flight)


                file.write(f"A/C TYPE: {aircraft_type}|CALLSIGN: {callsign}|ORIGIN: {origin_icao}|DESTINATION: {destination_icao}\n")

                status[0] += 1
            status[0] = total_flights[0]


# Parser
def parse_routes() -> RouteList:
    """
    parse airline routes information from data.txt
    """
    route_list = RouteList()

    config.REFRESH = True

    with open(FILE_DIR) as file:
        flights = file.readlines()[1:]
        for flight in flights:
            airline = Airline(config.CURRENT_AIRLINE)

            split_flight = flight.strip("\n").split("|")
            variables = get_flight_variables(split_flight)

            airline.set_parameters(variables[0], variables[1], variables[2], variables[3])

            route_list.add_routes(airline)
    
    config.AIRLINE_LIST = route_list