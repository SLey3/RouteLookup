# Imports
from pathlib import Path
from threading import Thread

from flask import (  # noqa: E501
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

import routeparser as rp
from Config import config
from form_validators import validate_live_search
from routeparser import generate_routes, init_file, parse_routes, refresh

# API routes
FOLDER_DIR = Path(__file__).resolve().parent / "templates" / "api"

# Routes
api = Blueprint(__name__, "api", url_prefix="/api", template_folder=FOLDER_DIR)

generate_thread = None


@api.route("/airlines", methods=["GET"])
def airlines():
    airlines = config.FLIGHTRADAR_API.get_airlines()

    airline_list = []

    for airline in airlines:
        airline_list.append((airline["Name"], airline["ICAO"]))

    return render_template("airlines.html", airlines=airline_list)


@api.route("/generate", methods=["POST"])
def generate():
    global generate_thread, status

    if request.method == "POST":
        parameters = request.args.to_dict()

        if "icao" in parameters.keys():
            if config.REFRESH:
                refresh()
                rp.status.clear()
                rp.status.append(0)
            init_file(parameters["icao"])

            generate_thread = Thread(target=generate_routes, args=(parameters["icao"],))
            return redirect(url_for("api.process_generation"))


@api.route("/generate/process", methods=["GET"])
def process_generation():
    generate_thread.start()

    return render_template(
        "process.html", total_flights=config.AIRLINE_FLIGHTS_LEN
    )  # noqa: E501


@api.route("/generate/status", methods=["GET"])
def generation_status():
    try:
        return jsonify({"status": rp.status[0]})
    except IndexError:
        return jsonify({"status": 0})


@api.route("/parse", methods=["GET"])
def parse_data():
    if request.method == "GET":
        parse_routes()

        return redirect(url_for("routes.main"))


@api.route("/validatesearch", methods=["POST"])
def active_search():
    args = request.get_data()
    args = str(args).split("=")
    args = {args[0].strip("b'"): args[1].strip("'")}

    res = {"invalid": False, "errors": [], "query": None}

    validate_resp = validate_live_search(args["query"])

    res["errors"] = validate_resp

    if validate_resp:
        res["invalid"] = True
    else:
        res["query"] = args["query"]

    return jsonify(res)
