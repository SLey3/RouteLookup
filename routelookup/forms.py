# imports
from FlightRadar24 import FlightRadar24API
from Config import config
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, ValidationError
from wtforms.widgets import html_params
from markupsafe import escape, Markup
from form_validators import AtLength

# widget and field
class NavigraphField(SubmitField):
    def __init__(self, part, *args, **kwargs):
        self.part = part
        super(NavigraphField, self).__init__(*args, **kwargs)

    def __call__(self,  **kwargs):
        kwargs = kwargs | self.render_kw
        kwargs.setdefault("type", "submit")

        if config.NAVIGRAPH_ENABLED == "Enabled":
            if self.part == 'Enable':
                kwargs['class'] = kwargs['class'] + " btn-secondary"
                params = html_params(disabled=True, aria_current="rg-enable", **kwargs)
            else:
                kwargs['class'] = kwargs['class'] + " btn-light"
                params = html_params(**kwargs)
        else:
            if self.part == 'Enable':
                kwargs['class'] = kwargs['class'] + " btn-light"
                params = html_params(**kwargs)
            else:
                kwargs['class'] = kwargs['class'] + " btn-secondary"
                params = html_params(disabled=True, aria_current="rg-disable", **kwargs)
        
        return Markup("<button %s>%s</button>" % (params, escape(self.render_kw["value"])))
    
    def process_data(self, data):
        if config.NAVIGRAPH_ENABLED == "Enabled":
            if self.id == "rg-enable":
                data = False
            else:
                data = True
        else:
            if self.id == "rg-disable":
                data = False
            else:
                data = True
        self.data = data

    def process_formdata(self, data):
        # bypass method as it is not needed
        pass

# forms
class AirlineInitForm(FlaskForm):
    initializer = StringField(validators=[
        InputRequired("Missing Input"),
        AtLength(3, "ICAO code")
    ], 
    id="airline-input",
    render_kw={
        "class" : "form-control-sm",
        "placeholder" : "Enter...",
        "aria-describedby" : "airline-help"
    })

    def add_validator_to(self, attr, *args):
        validator_attr = getattr(self, attr)

        if hasattr(validator_attr, "validators"):
            validator_attr.validators = validator_attr.validators + list(args)
        else:
            raise AttributeError("Check again if you inputed the correct attribute name.")

    submit_btn = SubmitField(id="airline-form-sbmt",
                             render_kw={"class" : "btn btn-dark mb-3",
                                        "value" : "Submit"})
    

class Config_FlightRadarUSRForm(FlaskForm):
    email = StringField( id="fr-un-input", validators=[Email("check if email is written correctly (correct email format)", check_deliverability=True)],
                        render_kw={
                            'class' : 'form-control-sm',
                            'placeholder' : 'Email'
                        })
    
    email_submit = SubmitField(id="fr-usr-sbmt", render_kw={
        'class' : 'btn btn-primary mb-3',
        'value' : 'Submit'
    })

    @staticmethod
    def validate_email(form, field):
        try:
            FlightRadar24API(field.data, config.FLIGHTRADAR_PASSWORD)
        except:
            raise ValidationError("Check if your email is the correct email from FlightRadar24.")

class Config_FlightRadarPWDForm(FlaskForm):
    pwd = PasswordField(id="fr-pwd-input", render_kw={
        'class' : 'form-control-sm',
        'placeholder' : 'Password'
    })

    pwd_submit = SubmitField(id="fr-pwd-sbmt", render_kw={
        'class' : 'btn btn-primary mb-3',
        'value' : 'Submit'
    })

    @staticmethod
    def validate_pwd(form, field):
        if len(field.data) < 7:
            raise ValidationError("Password must be at least 7 characters")
        try:
            FlightRadar24API(config.FLIGHTRADAR_USERNAME, field.data)
        except:
            raise ValidationError("Check if your password is the correct password from FlightRadar24") 
        
class Config_NavigraphEnableForm(FlaskForm):
    enable = NavigraphField("Enable",
                            id="rg-enable",
                            render_kw={
                                'name' : 'route-generation-true',
                                'value' : 'Enable',
                                'class' : 'btn'
                            })
    
    disable = NavigraphField("Disable",
                             id='rg-disable',
                             render_kw={
                                 'name' : 'route-generation-false',
                                 'value' : 'Disable',
                                 'class' : 'btn'
                             })