import logging
from flask_cors import CORS
from flask import Flask, json
from flask_hal import HAL, HALResponse
from chaosmonkey.api.attacks_blueprint import attacks
from chaosmonkey.api.executors_blueprint import executors
from chaosmonkey.api.planners_blueprint import planners
from chaosmonkey.api.plans_blueprint import plans
from chaosmonkey.api.api_errors import APIError

log = logging.getLogger(__name__)

# Create FlaskApp
flask_app = Flask("cm_api")
HAL(flask_app, HALResponse)
CORS(flask_app)

# Register blueprints
root = "/api/"
prev1 = root + "1"
flask_app.register_blueprint(executors, url_prefix=prev1 + "/executors")
flask_app.register_blueprint(plans, url_prefix=prev1 + "/plans")
flask_app.register_blueprint(attacks, url_prefix=prev1 + "/attacks")
flask_app.register_blueprint(planners, url_prefix=prev1 + "/planners")


# Register error handler for custom APIError exception
@flask_app.errorhandler(APIError)
def handle_invalid_usage(error):
    """
    Handler for APIErrors thrown by API endpoints
    """
    log.info('%d %s', error.status_code, error.message)
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
