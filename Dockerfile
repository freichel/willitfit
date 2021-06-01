FROM python:3.8.6-buster
COPY api /api
COPY willitfit /willitfit
COPY requirements.txt /requirements.txt 
#COPY credentials.json /credentials.json
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0 