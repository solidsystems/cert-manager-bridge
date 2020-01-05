FROM python:3.7

WORKDIR /app

COPY setup.py setup.py

RUN pip install .

COPY certbridge/ certbridge/

CMD ["python", "certbridge/__init__.py"]
