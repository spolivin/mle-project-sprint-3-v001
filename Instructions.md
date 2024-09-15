# Instructions to launch a microservice

## 1. FastAPI microservices in the virtual environment

In order to launch the applicates, one firstly needs to prepare the virtual environment and then run `uvicorn` server:

```bash
# Preparing virtual env
sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_fastapi_app
source .venv_fastapi_app/bin/activate
pip install -r services/requirements.txt

# Changing working dir
cd services

# Launching uvicorn server on port 1702
sh run_uvicorn_server.sh 1702
```

After successfully running the above commands, `uvicorn` server will be launched on http://localhost:1702 which can now be used to accept requests.

### Example of a curl-request to the application

Test request can be made by opening up a new terminal window and running a [*shell*-script](services/send_test_request.sh) which will send a request to the server on port 1702 for `flat_id=101`:

```bash
sh send_test_request.sh 1702 101
```
> NOTE: Before running the command one needs to make sure that the virtual environment is activated by `source .venv_fastapi_app/bin/activate`. 

It may take a bit of time for all the preprocessors to process the input data, afer which we will be able to see the server response in the terminal.

> Remark: After finishing working with the server, enter `Ctrl+C` to stop the application.

## 2. FastAPI microservice in a Docker-container

The following sequence of commands from the root directory will allow launching the application in a docker-container:
```bash
# Changing working dir
cd services

# Building the image
docker image build . --tag price-prediction-app --file Dockerfile_ml_service

# Running Docker container
docker container run --publish 4600:1702 --env-file .env price-prediction-app
```

Web interface of the FastAPI application will now be accessible from http://localhost:4600.

### Example of a curl-request to the the application

In order to send a new test request to the server we can reuse `send_test_request.sh` script with the arguments of the forwarded port and number of a flat from a new terminal window:

```bash
sh send_test_request.sh 4600 10900
```

> Remark: After finishing testing the container, it is recommended to run `docker container stop <container-id>` for stopping the container.

## 3. Docker compose for the microservice and monitoring system

For launching the application with the monitoring system *Prometheus* and *Grafana*, one needs to run the following commands from the root directory:

```bash
# Changing working dir
cd services

# Launching services via Docker Compose
docker compose up --build
```

### Example of a curl-request to the application

```bash
sh send_test_request.sh 1702 109
```

> Remark: After finishing working with the service, it is recommended to run `docker compose down` for stopping and deleting containers being run.

## 4. Script for simulating load

In order to simulate requests being sent to the service, we can use [`simulate_server_load.py`](services/simulate_service_load.py) script which generates 30 requests after each of which there is a 2 seconds pause and an additional 30 seconds pause after the 15-th sent request.

Script is launched from a new terminal:
```bash
python simulate_service_load.py --port 1702
```

Services addresses:
- Microservice: http://localhost:1702
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000


## 5. Loading a ready dashboard

In order to launch a finished dashboard in *Grafana*, one needs to complete the following steps after successfully launching the service via *Docker Compose*:

1. Go to http://localhost:3000 and get authorized using username and password from `services/.env`.
2. Specify *Prometheus* in *Data sources* with `http://prometheus:9090` address.
3. Run `python fix_datasource_uid.py` from the root directory in order to change the *UID* for the current *Grafana* session and loading the dashboard.
4. Go to *Dashboards* in *Grafana* and go to *New* -> *Import*. One now needs to simply copy and past the contents of `dashboard.json` and entering *Load*.
