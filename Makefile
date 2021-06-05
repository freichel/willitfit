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

#TBD

# ----------------------------------
#			GOOGLE CLOUD
# ----------------------------------

set_project:
	-@gcloud config set project ${PROJECT_ID}
