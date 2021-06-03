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
FRONT_END_FILE=willitfit/frontend/app.py
BACK_END_FILE=api.api
BACK_END_APP=app

# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* ${PROJECT_FOLDER}/*.py

black:
	@black scripts/* ${PROJECT_FOLDER}/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr ${PROJECT_FOLDER}-*.dist-info
	@rm -fr ${PROJECT_FOLDER}.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#            STREAMLIT/API
# ----------------------------------

run_streamlit:
	-@streamlit run ${FRONT_END_FILE}

run_api:
	@uvicorn ${PROJECT_FOLDER}.${BACK_END_FILE}:${BACK_END_APP} --reload

# Run with -j2 flag to execute simultaneously
run_full_interface: run_streamlit run_api
	
# ----------------------------------
#			GOOGLE CLOUD
# ----------------------------------

set_project:
	-@gcloud config set project ${PROJECT_ID}

create_bucket:
	-@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	-@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}