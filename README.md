# Deploying ML application to production 

## Description

After building and training the model from the previous steps for evaluating the flat prices, we now have to deploy the model to production.

### Business task

The model needs to be deployed to production and the service has to be developed in the following way:

* One should be able to obtain model predictions online;
* Service should be deployed flexibly - so that it would be possible to deploy it on different virtual machines where other services are already functioning;
* One needs to include the system of monitoring in order to in time warn of potential risks.

### ML Engineer task

1. Develop a FastAPI microservice.
2. Containerize the application using Docker.
3. Deploy a monitoring system using Prometheus and Grafana.
4. Develop a dashboard for monitoring in Grafana.
