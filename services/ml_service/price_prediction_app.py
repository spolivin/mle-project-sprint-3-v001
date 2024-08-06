"""FastAPI application for price prediction."""

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
from fastapi import FastAPI, Body
from .fast_api_handler import FastApiHandler


# Instantiating a FastAPI application
app = FastAPI()

# Enabling Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Instantiating a request handler
app.handler = FastApiHandler()

# Metric 1 to be exported
main_app_predictions = Histogram(
    "main_app_predictions",
    "Histogram of predictions",
    buckets=(3_000_000, 5_000_000, 7_000_000, 9_000_000, 11_000_000, 15_000_000)
)

# Metric 2 to be exported
main_app_counter_pos = Counter("main_app_counter_pos", "Count of high price evaluations")

@app.get("/")
def start_page() -> dict:
    """Displays a message when sending a GET-request."""
    return {
        "status": "OK",
        "task": "price-prediction",
        "model": "catboost",
        "preprocessing": ["sklearn", "autofeat"],
    }

@app.post("/api/price/") 
def get_prediction_for_item(
    flat_id: str,
    model_params: dict = Body(
        example = {
            "building_type_int": 2,
            "latitude": 55,
            "longitude": 33,
            "ceiling_height": 2,
            "flats_count": 200,
            "floors_total": 10,
            "has_elevator": True,
            "floor": 30,
            "kitchen_area": 1,
            "living_area": 10,
            "rooms": 2,
            "is_apartment": False,
            "total_area": 90,
        }
    )
) -> dict:
    """Displays a price-prediction result when sending a POST-request.

    Args:
        flat_id (str): Flat identifier.
        model_params (dict): Flat features for making a prediction.

    Returns:
        dict: Price prediction for a flat.
    """
    # Setting request parameters
    all_params = {
        "flat_id": flat_id,
        "model_params": model_params
    }

    # Receiving a server response
    server_response = app.handler.handle(all_params)

    # Tracking Metric 1
    price_prediction = server_response["prediction"]
    main_app_predictions.observe(price_prediction)

    # Tracking Metric 2
    if price_prediction > 10_000_000:
        main_app_counter_pos.inc()

    return server_response
