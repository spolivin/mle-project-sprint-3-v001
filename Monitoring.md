# Monitoring

Dashboard can be seen after launching the service via *Docker Compose* or by looking at `app_dashboard.jpg`.

Monitoring is based on tracking infrastructure metrics (e.g. RAM/CPU usage) as well as service-level metrics (e.g absolute/relative change of request processing time) and real-time metrics (in this case are represented by model predictions after a series of requests to the API).

## Monitoring layers

### Infrastructural layer:
- **RAM Usage**

This metric has been chosen due the fact that when developing an application it is essential to keep track of the resources usage. Graph of *Gauge* type is used, since in this case it is visually easier to control the RAM usage of the application.

- **CPU Usage**

This metric has been chosen, since when developing an application it is vital to control the way the processor is overloaded during requests handling. 


### Real-time metrics:
- **Prediction Quantiles**

This metric has been chosen, since the service includes a trained model which may at some point start outputting unreasonable results on some input data. Thus, in order to keep track of this, we are computing model prediction quantiles (5%, 50% and 95%). 

- **Number of high evaluations**

This metric has been chosen, since it may be interesting how many flats the model would evaluate with price higher than 10 million.

### Service-level metrics:

- **Request duration change / min** and **Number of requests / min**

These metrics are used to collecting data about the service itself.
