import flask
import waitress


app = flask.Flask('certbridge')


@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200


@app.route('/domain')
def domain():
    print(flask.headers)
    print(flask.request)
    return '{}', 400


waitress.serve(app, listen='*:8080')
