# _RouteLookup_ V1.0

This website brings in a tool for flight simulator users to be able to decide a route to take by allowing them to input the airline ICAO code and recieve a list of all available routes taken from FlightRader24, organizing the data by: 
1) aircraft type (in ICAO form)
2) callsign
3) origin airport (in ICAO form)
4) destination airport (in ICAO form)

## Requirements
- Python 3.9+
   
## Installation
1) clone the repository
2) run `configure_ip.py` (read instructions inside of the file for further instructions on running it)
3) remove ".base" from `.env.base`
4) Configure following values within `.env`:
   1) `FLIGHTRADAR_USERNAME=<value>` | you must have a flightradar24 account, the username must be the email
   2) `FLIGHTRADAR_PASSWORD=<value>` | enter flightradar24 account password
   3) `SECRET_KEY` | Some modules used by this program may require a secret key

## Usage
run the following command to run the website:
```
python routelookup/app.py
```