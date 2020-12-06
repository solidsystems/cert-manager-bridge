import os
import subprocess
import sys
from pprint import pprint

import flask
import waitress

app = flask.Flask('certbridge')

def info(msg):
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200


@app.route('/domain', methods=['POST', 'GET'])
def domain():
    info(dict(flask.request.headers))
    info(dict(flask.request.args))

    # /domain?path={$serverid}/webapps/{$appid}/{$path}&token=abc123

    expected = os.environ.get("DOMAIN_TOKEN")

    if expected:
        token = flask.request.args.get("token", None)
        if isinstance(token, list):
            token = token.pop()
        if token != expected:
            info(f"token equals {token}")
            flask.abort(400)

    host = flask.request.get_data().decode("utf-8")

    if '=' not in host:
        info(host)
        flask.abort(400)

    host = host.split('=')[1]

    # Misc ingress variables
    namespace = os.environ.get("ING_NAMESPACE")
    service = os.environ.get("ING_SERVICE")
    service_port = os.environ.get("ING_PORT")

    k8s = f"""
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: {host}
  namespace: {namespace}
  annotations:
    external-dns.alpha.kubernetes.io/cloudflare-proxied: "false"
    cert-manager.io/cluster-issuer: letsencrypt-prod-http
    kubernetes.io/tls-acme: "true"
spec:
  rules:
    - host: "{host}"
      http:
        paths:
          - path: /
            backend:
              serviceName: {service}
              servicePort: {service_port}
  tls:
    - hosts:
        - "{host}"
      secretName: {host}-cert
"""

    with open(f"/mnt/certbridge/{host}.yaml", "w") as fd:
        fd.write(k8s)

    # Create the cert for the custom mapped domain
    subprocess.Popen(["kubectl", "apply", "-f", f"/mnt/certbridge/{host}.yaml"])

    # DO spaces upload
    SPACES_ACCESS_KEY_ID = os.environ.get("SPACES_ACCESS_KEY_ID")
    SPACES_SECRET_ACCESS_KEY = os.environ.get("SPACES_SECRET_ACCESS_KEY")
    BUCKET_PATH = os.environ.get("BUCKET_PATH")
    subprocess.Popen(["s3cmd", f"--access_key={SPACES_ACCESS_KEY_ID}", f"--secret_key={SPACES_SECRET_ACCESS_KEY}", "put", f"/mnt/certbridge/{host}.yaml", f"{BUCKET_PATH}"])

    return '{}', 200

info("Starting server process...")
waitress.serve(app, listen='*:8080')
