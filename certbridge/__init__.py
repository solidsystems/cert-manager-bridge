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

    host = flask.request.get_json(force=True)
    host = host['name']

    k8s = f"""
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: {host}
  namespace: external-wordpress2
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
              serviceName: external-wordpress
              servicePort: 80
  tls:
    - hosts:
        - "{host}"
      secretName: {host}-cert
"""

    with open(f"/mnt/certbridge/{host}.yaml", "w") as fd:
        fd.write(k8s)

    return '{}', 200


waitress.serve(app, listen='*:8080')
