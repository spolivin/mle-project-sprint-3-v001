"""FastApiHandler class for processing API-requests."""

from catboost import CatBoostRegressor

from .preprocessing import preprocess_flat_features


class FastApiHandler:
    """Class for processing the request and returning a prediction."""

    def __init__(self) -> None:
        """Initializes class variables."""

        # Parameter types for validating request
        self.param_types = {"flat_id": str, "model_params": dict}

        # Loading the trained model
        self.model_path = "models/catboost_model.cbm"
        self.load_prediction_model(model_path=self.model_path)

        # Mandatory parameters for making a prediction
        self.required_model_params = [
            "building_type_int",
            "latitude",
            "longitude",
            "ceiling_height",
            "flats_count",
            "floors_total",
            "has_elevator",
            "floor",
            "kitchen_area",
            "living_area",
            "rooms",
            "is_apartment",
            "total_area",
        ]

    def load_prediction_model(self, model_path: str) -> None:
        """Loads the trained model.

        Args:
            model_path (str): Path to a model.
        """
        try:
            self.model = CatBoostRegressor()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def predict_flat_price(self, model_params: dict) -> float:
        """Predicts a price of a flat.

        Args:
            model_params (dict): Model parameters.

        Returns:
            float - price of a flat.
        """
        # Preparing the model parameters for the model
        preprocessed_features = preprocess_flat_features(flat_features=model_params)
        price_prediction = self.model.predict(preprocessed_features)[0]

        return price_prediction

    def check_required_query_params(self, query_params: dict) -> bool:
        """Validates query params.

        Args:
            query_params (dict): Request parameters.

        Returns:
            bool: True - if all query params present, False - else
        """
        if "flat_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["flat_id"], self.param_types["flat_id"]):
            return False

        if not isinstance(
            query_params["model_params"], self.param_types["model_params"]
        ):
            return False

        return True

    def check_required_model_params(self, model_params: dict) -> bool:
        """Validates model params.

        Args:
            model_params (dict): Flat's features for making a prediction.

        Returns:
            bool: True - if all model params present, False - else
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True

        return False

    def validate_params(self, params: dict) -> bool:
        """Validates a query.

        Args:
            params (dict): Parameters of a query.

        Returns:
            bool: True - if all query/model params present, False - else
        """
        # Verifying query parameters
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False

        # Verifying model parameters
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False

        return True

    def handle(self, params) -> dict:
        """Processes incoming API-request.

        Args:
            params (dict): Query params.

        Returns:
            dict: Result of a query.
        """
        try:
            # Displaying error in case of params issue
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            # Making a prediction in case of absence of errors
            else:
                model_params = params["model_params"]
                flat_id = params["flat_id"]
                print(
                    f"Predicting for flat_id: {flat_id} and model_params:\n{model_params}"
                )
                # Retrieving a model prediction and creating a response
                price_prediction = self.predict_flat_price(model_params)
                response = {
                    "flat_id": flat_id,
                    "prediction": round(price_prediction, 3),
                }
        # Displaying error in case of request issue
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        # Displaying a response
        else:
            return response
