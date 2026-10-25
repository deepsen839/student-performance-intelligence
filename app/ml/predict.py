from pathlib import Path

import joblib
import pandas as pd

from app.ml.features import (
    FEATURE_COLUMNS,
    build_student_features,
)


MODEL_FILE = Path(
    "app/ml/models/risk_model.joblib"
)


def load_model():

    if not MODEL_FILE.exists():

        raise FileNotFoundError(
            "Risk model not found. "
            "Run the training command first."
        )

    return joblib.load(
        MODEL_FILE
    )


def predict_risk_from_features(
    feature_row: dict,
) -> dict:
    """
    Predict risk from an already constructed
    feature vector.
    """

    model = load_model()

    X = pd.DataFrame(
        [feature_row]
    )

    X = X[
        FEATURE_COLUMNS
    ]

    probability = model.predict_proba(
        X
    )[0][1]

    risk_score = round(
        float(probability * 100),
        2,
    )

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


def predict_student_risk(
    df: pd.DataFrame,
    student_id: str,
) -> dict:
    """
    Build features for a student and predict
    performance decline risk.
    """

    student_df = df[
        df["student_id"] == student_id
    ].copy()

    if student_df.empty:

        raise ValueError(
            f"Student not found: {student_id}"
        )

    feature_row = (
        build_student_features(
            student_df
        )
    )

    prediction = (
        predict_risk_from_features(
            feature_row
        )
    )

    return {
        "student_id": student_id,
        "features": feature_row,
        **prediction,
    }