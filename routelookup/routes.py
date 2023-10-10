# Imports
from flask import Blueprint, render_template, redirect, url_for, request
from FlightRadar24 import FlightRadar24API
from Config import config as cg
from pathlib import Path
from forms import (
    AirlineInitForm, Config_FlightRadarPWDForm, Config_FlightRadarUSRForm,
    Config_NavigraphEnableForm
    )
from form_validators import AirlineICAORequired

# routes
FOLDER_DIR = Path(__file__).resolve().parent / 'templates'
STATIC_DIR = Path(__file__).resolve().parent / 'static'

routes = Blueprint(__name__, 'routes', template_folder=FOLDER_DIR, static_folder=STATIC_DIR)

@routes.route('/', methods=['GET'])
def main_redirect():
    return redirect(url_for('routes.main'))

@routes.route('/', methods=['GET', 'POST'], subdomain='application')
def main():
    form = AirlineInitForm()

    form.add_validator_to(
        "initializer", 
        AirlineICAORequired(f'''
        Must be an airline ICAO code. Please refer to: <a id="err-icao" href="{url_for("api.airlines")}" class="link-danger">List of Airlines</a> for a list of airlines with ICAO codes listed.
        ''')
    )
    
    if form.validate_on_submit():
        icao = form.initializer.data

        return redirect(url_for('api.generate', icao=icao), code=307)

    return render_template('main.html', initializer_form=form)

@routes.route('/config', methods=['GET'], subdomain='application')
def config_redirect():
    return redirect(url_for('routes.config'))

@routes.route("/config", methods=['GET', 'POST'])
def config():
    usr_form = Config_FlightRadarUSRForm()
    pwd_form = Config_FlightRadarPWDForm()
    navigraph_form = Config_NavigraphEnableForm()
    if request.method == 'POST':
        if usr_form.data['email']:
            if usr_form.validate():
                cg.FLIGHTRADAR_USERNAME = usr_form.email.data
                cg.FLIGHTRADAR_API = FlightRadar24API(cg.FLIGHTRADAR_USERNAME, cg.FLIGHTRADAR_PASSWORD)
        elif pwd_form.data['pwd']:
            if pwd_form.validate():
                cg.FLIGHTRADAR_PASSWORD = pwd_form.pwd.data
        elif navigraph_form.enable.data:
            cg.NAVIGRAPH_ENABLED = "Enabled"
        elif navigraph_form.disable.data:
            cg.NAVIGRAPH_ENABLED = "Disabled"
    return render_template('config.html', usr_form=usr_form, pwd_form=pwd_form, navigraph_form=navigraph_form)