FROM python:3.8.6-buster

# Choose port
EXPOSE 8501

# Copy requirements as well as entire project folder
COPY requirements.txt /requirements.txt
COPY willitfit /willitfit

# Install packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Install Chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set Python path to be able to import project as module
ENV PYTHONPATH "/"

# First line may not be needed now
CMD uvicorn willitfit.api.api:app --host 0.0.0.0 --port $PORT
# Run Streamlit front end
CMD streamlit run willitfit/frontend/app.py