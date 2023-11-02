# imports
import re

from wtforms.validators import ValidationError

from routeparser import get_airline


# validators
def AirlineRequired(url):
    """
    Validates whether the form data matches a valid airline or not
    """
    message = f"""Must be an airline ICAO code.
    Please refer to:
    <a id="err-icao" href="{url}" class="link-danger">List of Airlines</a>
    for a list of airlines with ICAO codes listed."""

    def _airline(form, field):
        airline = get_airline(field.data)

        if not airline:
            raise ValidationError(message)

    return _airline


def AtLength(length: int, start_message=None):
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


def validate_live_search(text: str):
    search_rgx = re.compile(r"[A-Z\d]+", re.A | re.IGNORECASE)

    regex_err_msg = "There must not be special characters (e.g. #, !, ?, etc)"

    err_list = []

    if not search_rgx.fullmatch(text) and len(text):
        err_list.append(regex_err_msg)
    else:
        err_list.remove(regex_err_msg) if regex_err_msg in err_list else ...

    return err_list
