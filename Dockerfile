FROM python:3.14.0a3-slim

ENV DOCTL_VERSION=1.34.0
ENV KUBE_VERSION=1.17.0

# Dependencies
RUN apt-get update && apt-get install -yq curl libmagic-dev

# Install certbridge
WORKDIR /app
COPY setup.py setup.py
RUN pip install .
COPY certbridge/ certbridge/

# Install doctl
RUN curl -L https://github.com/digitalocean/doctl/releases/download/v${DOCTL_VERSION}/doctl-${DOCTL_VERSION}-linux-amd64.tar.gz  | tar xz
RUN mv doctl /usr/local/bin

# Install s3cmd
RUN pip3 install s3cmd
COPY s3cfg /root/.s3cfg

# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

CMD ["python", "certbridge/__init__.py"]
