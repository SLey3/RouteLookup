# imports
from flask import Flask
from routes import routes
from api import api
from routeparser import reset_contents, fr_api_logout
from Config import config
import atexit

# application
app = Flask(__name__)
app.config.from_object(config)
app.add_template_global(config)

# register after process instructions
if not config.DEVELOPMENT and config.DEBUG:
    atexit.register(reset_contents)
atexit.register(fr_api_logout)
atexit.register(config.cleanup_after_shutdown)

# register blueprint
app.register_blueprint(routes)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()