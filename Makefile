# ----------------------------------
#           PARAMETERS
# ----------------------------------

# General
PROJECT_FOLDER=willitfit

# Google
PROJECT_ID=willitfit
BUCKET_NAME=willitfit-bucket
BUCKET_FOLDER=data
REGION=europe-west3
PYTHON_VERSION=3.8.6
PACKAGE_NAME=willitfit

# Streamlit/API
FRONT_END_FILE=willitfit/frontend/frontend.py
BACK_END_FILE=api.api
BACK_END_APP=app

# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip freeze --exclude-editable | xargs -r pip uninstall -y 
	@pip install -r requirements.txt

# ----------------------------------
#            STREAMLIT/API
# ----------------------------------

start_app:
	-@streamlit run ${FRONT_END_FILE}

# ----------------------------------
#			  DOCKER
# ----------------------------------

docker_build:
	@echo "Building new Docker image "$(img)"..."
	@echo "Restarting Docker service. Enter password if prompted..."
	@sudo service docker stop
	@sudo service docker start
	@echo "Docker service running."
	@echo "Building image "$(img)" now..."
	@docker build -f Dockerfile -t $(img) .
	@echo "Image $(img) built."

docker_run:
	@echo "Launching Docker image $(img) locally on port 8501 (http://localhost:8501/)..."
	@docker run -p 8501:8501 $(img)


# ----------------------------------
#			GOOGLE CLOUD
# ----------------------------------

set_project:
	-@gcloud config set project ${PROJECT_ID}
