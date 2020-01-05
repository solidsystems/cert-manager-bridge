import flask
import waitress
from pprint import pprint


app = flask.Flask('certbridge')


@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200


@app.route('/domain', methods=['POST', 'GET'])
def domain():
    pprint(dict(flask.request.headers))
    pprint(dict(flask.request.args))
    pprint(flask.request.get_data())
    return '{}', 400


waitress.serve(app, listen='*:8080')
