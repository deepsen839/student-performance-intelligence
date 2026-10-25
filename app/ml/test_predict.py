from app.data.loader import load_assessments
from app.ml.train import (
    create_training_data,
)
from app.ml.predict import predict_risk


def main():

    df = load_assessments()

    training_df = create_training_data(
        df
    )

    # Pick first student
    row = training_df.iloc[0]

    feature_row = {
        column: row[column]
        for column in [
            "overall_score",
            "recent_score",
            "previous_score",
            "accuracy",
            "trend_slope",
            "improvement",
            "weak_topic_count",
            "average_time_taken",
            "attempt_rate",
        ]
    }

    result = predict_risk(
        feature_row
    )

    print("=" * 60)
    print("STUDENT RISK PREDICTION")
    print("=" * 60)

    print(
        f"Risk Score: "
        f"{result['risk_score']}%"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )


if __name__ == "__main__":
    main()