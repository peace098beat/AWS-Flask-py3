import json
from flask import Blueprint, Response, current_app

# apisのBlueprint
apis = Blueprint('apis', __name__, url_prefix='/api')





@apis.route('/', methods=['GET'])
def apis_get():
    logger = current_app.logger
    logger.debug('open apis')
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@apis.route('/', methods=['POST'])
def apis_post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)