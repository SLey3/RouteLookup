# imports
from routeparser import get_airline
from wtforms.validators import ValidationError

# validators
def AirlineICAORequired(msg = None):
    """
    Validates whether string is a valid ICAO code
    """
    if isinstance(msg, str):
        message = msg
    else:
        message = "Must be an airline ICAO code. Please double check to make sure it's correct."

    def _airlineicao(form, field):
        airline = get_airline(field.data)
        
        if not airline:
            raise ValidationError(message)
    return _airlineicao


def AtLength(length: int, start_message = None):
    """
    Make's sure input is exactly at specified character length
    """
    if not isinstance(start_message, str):
        message = f"Must be exactly {length} characters long"
    else:
        message = f"{start_message} must be exactly {length} characters long"

    def _atlength(form, field):
        if len(field.data) != length:
            raise ValidationError(message)
    
    return _atlength