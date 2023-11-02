# Imports
from pathlib import Path

from flask import Blueprint, redirect, render_template, request, url_for
from FlightRadar24 import FlightRadar24API

from Config import config as cg
from form_validators import AirlineRequired
from forms import (
    AirlineInitForm,
    Config_FlightRadarPWDForm,
    Config_FlightRadarUSRForm,
    Config_NavigraphEnableForm,
    Config_RefreshTable,
)
from routeparser import get_airline

# routes
FOLDER_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

routes = Blueprint(
    __name__, "routes", template_folder=FOLDER_DIR, static_folder=STATIC_DIR
)


@routes.route("/", methods=["GET"])
def main_redirect():
    return redirect(url_for("routes.main"))


@routes.route("/", methods=["GET", "POST"], subdomain="application")
def main():
    init_form = AirlineInitForm()

    init_form.add_validator_to("initializer", AirlineRequired(url_for("api.airlines")))

    if init_form.validate_on_submit():
        icao = get_airline(init_form.initializer.data.capitalize())["ICAO"]

        return redirect(url_for("api.generate", icao=icao), code=307)

    return render_template("main.html", initializer_form=init_form)


@routes.route("/config", methods=["GET"], subdomain="application")
def config_redirect():
    return redirect(url_for("routes.config"))


@routes.route("/config", methods=["GET", "POST"])
def config():
    usr_form = Config_FlightRadarUSRForm()
    pwd_form = Config_FlightRadarPWDForm()
    navigraph_form = Config_NavigraphEnableForm()
    refresh_form = Config_RefreshTable()

    if request.method == "POST":
        if usr_form.email_submit.data:
            if usr_form.validate():
                cg.FLIGHTRADAR_USERNAME = usr_form.email.data
                cg.FLIGHTRADAR_API = FlightRadar24API(
                    cg.FLIGHTRADAR_USERNAME, cg.FLIGHTRADAR_PASSWORD
                )
        elif pwd_form.pwd_submit.data:
            if pwd_form.validate():
                cg.FLIGHTRADAR_PASSWORD = pwd_form.pwd.data
                cg.FLIGHTRADAR_API = FlightRadar24API(
                    cg.FLIGHTRADAR_USERNAME, cg.FLIGHTRADAR_PASSWORD
                )
        elif refresh_form.refresh.data:
            if cg.CURRENT_AIRLINE:
                return redirect(
                    url_for("api.generate", icao=cg.CURRENT_AIRLINE["ICAO"]), code=307
                )
            else:
                refresh_form.refresh.errors = ("No current data detected.",)
        elif (
            navigraph_form.enable.data
            and not usr_form.email_submit.data
            and not pwd_form.pwd_submit.data
        ):
            cg.NAVIGRAPH_ENABLED = "Enabled"
        elif navigraph_form.disable.data:
            cg.NAVIGRAPH_ENABLED = "Disabled"
    return render_template(
        "config.html",
        usr_form=usr_form,
        pwd_form=pwd_form,
        navigraph_form=navigraph_form,
        refresh_form=refresh_form,
    )
