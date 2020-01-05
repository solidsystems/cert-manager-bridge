import flask
import waitress


app = flask.Flask('certbridge')


@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200


@app.route('/domain')
def domain():
    return 'UNCONFIGURED', 400


waitress.serve(app, listen='*:8080')
