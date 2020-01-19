import flask
import os
import subprocess
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

    #https://certbridge.mentormakers.club/domain?path={$serverid}/webapps/{$appid}/{$path}

    host = flask.request.get_data().split(b'=')[1].decode("utf-8")

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

    # Create the cert for the custom mapped domain
    # kubectl_cmd = f"kubectl apply -f /mnt/certbridge/{host}.yaml"
    # os.system(kubectl_cmd)
    subprocess.Popen("kubectl", "apply", "-f", f"/mnt/certbridge/{host}.yaml")

    # DO spaces upload
    SPACES_ACCESS_KEY_ID = os.environ.get("SPACES_ACCESS_KEY_ID")
    SPACES_SECRET_ACCESS_KEY = os.environ.get("SPACES_SECRET_ACCESS_KEY")
    BUCKET_PATH = os.environ.get("BUCKET_PATH")
    # do_upload_cmd = f"s3cmd --access_key={SPACES_ACCESS_KEY_ID} --secret_key={SPACES_SECRET_ACCESS_KEY} put '/mnt/certbridge/{host}.yaml' {BUCKET_PATH}"
    # os.system(do_upload_cmd)
    subprocess.Popen(["s3cmd", f"--access_key={SPACES_ACCESS_KEY_ID}", f"--secret_key={SPACES_SECRET_ACCESS_KEY}", "put", f"/mnt/certbridge/{host}.yaml", f"{BUCKET_PATH}"])

    return '{}', 200


waitress.serve(app, listen='*:8080')
