# Imports
from flask import Blueprint, render_template,  redirect, url_for, request, jsonify
from routeparser import parse_routes, generate_routes, init_file, refresh
from Config import config
from pathlib import Path
from threading import Thread
import routeparser as rp

# API routes
FOLDER_DIR = Path(__file__).resolve().parent / 'templates' / 'api'

api = Blueprint(__name__, 'api', url_prefix='/api', template_folder=FOLDER_DIR)

generate_thread = None

@api.route("/airlines", methods=['GET'])
def airlines():
    airlines = config.FLIGHTRADAR_API.get_airlines()

    airline_list = []

    for airline in airlines:
        airline_list.append((airline['Name'], airline['ICAO']))

    return render_template('airlines.html', airlines=airline_list)

@api.route("/enablenavigraph", methods=['POST'])
def enable_navigraph():
    if request.method == 'POST':
        data = request.form # or request.data CHECK for correct one


@api.route("/generate", methods=['POST'])
def generate():
    global generate_thread, status

    if request.method == 'POST':
        parameters = request.args.to_dict()

        if "icao" in parameters.keys():
            if config.REFRESH:
                refresh()
                rp.status.clear()
                rp.status.append(0)
            init_file(parameters["icao"])

            generate_thread = Thread(target=generate_routes, args=(parameters["icao"],))
            return redirect(url_for('api.process_generation'))

@api.route("/generate/process", methods=['GET'])
def process_generation():
    generate_thread.start()

    return render_template('process.html', total_flights=config.AIRLINE_FLIGHTS_LEN)

@api.route("/generate/status", methods=['GET'])
def generation_status():
    try:
        return jsonify({"status" : rp.status[0]})
    except IndexError:
        return jsonify({"status" : 0})


@api.route("/parse", methods=['GET'])
def parse_data():
    if request.method == 'GET':
        parse_routes()
        
        return redirect(url_for("routes.main"))
        
