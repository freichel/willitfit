FROM python:3.8.6-buster

COPY requirements.txt /requirements.txt
COPY willitfit /willitfit

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn willitfit.api.api:app --host 0.0.0.0 --port $PORT