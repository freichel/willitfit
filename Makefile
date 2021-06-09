# ----------------------------------
#           PARAMETERS
# ----------------------------------

# General
PROJECT_FOLDER=willitfit
PORT=8501

# Google
PROJECT_ID=willitfit
BUCKET_NAME=willitfit-bucket
BUCKET_FOLDER=data
REGION=europe-west3
PYTHON_VERSION=3.8.6
PACKAGE_NAME=willitfit
MEMORY=8G
CPU=4

# Streamlit/API
FRONT_END_FILE=willitfit/frontend/frontend.py
BACK_END_FILE=api.api
BACK_END_APP=app

DB=cloud

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
	@echo "Starting app using "${DB}" database."
	@echo "Use 'make DB=local start_app' to use local database"
	-@streamlit run ${FRONT_END_FILE} ${DB}

# ----------------------------------
#			  DOCKER
# ----------------------------------

docker_build:
    ifeq ($(mode),GC)
		@echo "Building new Docker image eu.gcr.io/"$(PROJECT_ID)"/"$(img)" for GC deployment..."
    else
		@echo "Building new Docker image "$(img)"..."
    endif
	@echo "Restarting Docker service. Enter password if prompted..."
	@sudo service docker start
	@echo "Docker service running."
	@echo "Building image now..."
    ifeq ($(mode),GC)
		@docker build -f Dockerfile -t eu.gcr.io/$(PROJECT_ID)/$(img) .
		@echo "Image eu.gcr.io/"$(PROJECT_ID)"/"$(img)" built for GC deployment."
    else
		@docker build -f Dockerfile -t $(img) .
		@echo "Image $(img) built."
    endif

docker_run:
	@echo "Launching Docker image $(img) locally on port "$(PORT)" (http://localhost:"$(PORT)"/)..."
	@docker run -p $(PORT):$(PORT) $(img)

docker_build_run_deploy:
    ifeq ($(mode),GC)
		@echo "Building and deploying new Docker image eu.gcr.io/"$(PROJECT_ID)"/"$(img)"..."
		@echo "Building new Docker image eu.gcr.io/"$(PROJECT_ID)"/"$(img)" for GC deployment..."
    else
		@echo "Building and running new Docker image "$(img)" locally..."
		@echo "Building new Docker image "$(img)"..."
    endif
	@echo "Restarting Docker service. Enter password if prompted..."
	@sudo service docker start
	@echo "Docker service running."
	@echo "Building image "$(img)" now..."
    ifeq ($(mode),GC)
		@docker build -f Dockerfile -t eu.gcr.io/$(PROJECT_ID)/$(img) .
		@echo "Image eu.gcr.io/"$(PROJECT_ID)"/"$(img)" built for GC deployment."
		@docker push eu.gcr.io/$(PROJECT_ID)/$(img)
		@gcloud run deploy --image eu.gcr.io/$(PROJECT_ID)/$(img) --memory $(MEMORY) --cpu $(CPU) --platform managed --region europe-west3 --port $(PORT)
    else
		@docker build -f Dockerfile -t $(img) .
		@echo "Image $(img) built."
		@echo "Launching Docker image $(img) locally on port $(PORT) (http://localhost:"$(PORT)"/)..."
		@docker run -p $(PORT):$(PORT) $(img)
    endif
