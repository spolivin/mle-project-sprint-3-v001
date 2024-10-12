import joblib

import pandas as pd


def load_preprocessor(preprocessor_path: str) -> None:
    """Loads the preprocessor."""

    with open(preprocessor_path, "rb") as fd:
        preprocessor = joblib.load(fd)

    return preprocessor


def preprocess_flat_features(flat_features: dict) -> pd.DataFrame:
    """Prepares the data for a model input.

    Args:
        flat_features (dict): Features of a flat.

    Returns:
        pd.DataFrame - DataFrame of preprocessed data.
    """

    # Transforming dict of features into DataFrame of features
    flat_features_df = pd.DataFrame(flat_features, index=[0])

    # Loading preprocessors
    sklearn_preprocessor = load_preprocessor(
        preprocessor_path="models/sklearn_preprocessor.pkl",
    )
    autofeat_preprocessor = load_preprocessor(
        preprocessor_path="models/autofeat_preprocessor.pkl",
    )

    # Preprocessing using Sklearn's estimator
    flat_features_prepared_sklearn = sklearn_preprocessor.transform(flat_features_df)
    flat_features_prepared_sklearn = pd.DataFrame(
        flat_features_prepared_sklearn,
        columns=sklearn_preprocessor.get_feature_names_out(),
    )

    # Preprocessing using Autofeat's preprocessor
    flat_features_prepared_autofeat = autofeat_preprocessor.transform(flat_features_df)

    # Joining the results together
    flat_features_prepared = pd.concat(
        [
            flat_features_prepared_sklearn,
            flat_features_prepared_autofeat[autofeat_preprocessor.new_feat_cols_],
        ],
        axis=1,
    )

    return flat_features_prepared
