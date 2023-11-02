# imports
import atexit

from flask import Flask
from flask_cors import CORS

from api import api
from Config import config
from routeparser import fr_api_logout, reset_contents
from routes import routes

# application
app = Flask(__name__)
app.config.from_object(config)
app.add_template_global(config)

CORS(app)

# register after process instructions
if not config.DEVELOPMENT and not config.DEBUG:
    atexit.register(reset_contents)
else:
    atexit.register(reset_contents, True)
atexit.register(fr_api_logout)
atexit.register(config.cleanup_after_shutdown)

# registsqer blueprint
app.register_blueprint(routes)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run()
