UVICORN_SERVER_PORT="${1}"

uvicorn ml_service.price_prediction_app:app --port "$UVICORN_SERVER_PORT" --host 0.0.0.0