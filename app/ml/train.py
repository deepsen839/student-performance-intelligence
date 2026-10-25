from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from app.data.loader import load_assessments


MODEL_DIR = Path("app/ml/models")

MODEL_FILE = (
    MODEL_DIR / "risk_model.joblib"
)


FEATURE_COLUMNS = [
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


def create_training_data(
    df: pd.DataFrame,
):
    """
    Create training features and target.

    We use the first 7 assessments as historical
    information and assess whether performance declines
    in the final 3 assessments.
    """

    rows = []

    for student_id in df[
        "student_id"
    ].unique():

        student_df = (
            df[
                df["student_id"] == student_id
            ]
            .sort_values("attempt_date")
            .reset_index(drop=True)
        )

        if len(student_df) < 7:
            continue

        # ---------------------------------------------
        # Historical assessments
        # ---------------------------------------------

        history = student_df.iloc[:7]

        # Future assessments
        future = student_df.iloc[7:]

        # ---------------------------------------------
        # Historical score
        # ---------------------------------------------

        overall_score = (
            history["score_percentage"]
            .mean()
        )

        recent_score = (
            history.tail(3)[
                "score_percentage"
            ].mean()
        )

        previous_score = (
            history.head(3)[
                "score_percentage"
            ].mean()
        )

        # ---------------------------------------------
        # Accuracy
        # ---------------------------------------------

        total_attempted = (
            history[
                "questions_attempted"
            ].sum()
        )

        total_correct = (
            history[
                "questions_correct"
            ].sum()
        )

        accuracy = (
            total_correct
            / total_attempted
            * 100
            if total_attempted > 0
            else 0
        )

        # ---------------------------------------------
        # Simple trend
        # ---------------------------------------------

        from sklearn.linear_model import (
            LinearRegression,
        )

        X = (
            history.index.values
            .reshape(-1, 1)
        )

        y = history[
            "score_percentage"
        ].values

        trend_model = LinearRegression()

        trend_model.fit(
            X,
            y,
        )

        trend_slope = float(
            trend_model.coef_[0]
        )

        # ---------------------------------------------
        # Improvement
        # ---------------------------------------------

        improvement = (
            recent_score
            - previous_score
        )

        # ---------------------------------------------
        # Weak topics
        # ---------------------------------------------

        topic_scores = (
            history
            .groupby("topic")[
                "score_percentage"
            ]
            .mean()
        )

        weak_topic_count = int(
            (topic_scores < 50).sum()
        )

        # ---------------------------------------------
        # Time / attempt rate
        # ---------------------------------------------

        average_time_taken = (
            history["time_taken"]
            .mean()
        )

        attempt_rate = (
            history[
                "questions_attempted"
            ].sum()
            / (
                len(history) * 30
            )
            * 100
        )

        # ---------------------------------------------
        # Future performance
        # ---------------------------------------------

        future_score = (
            future["score_percentage"]
            .mean()
        )

        # Decline threshold
        decline = (
            future_score
            < recent_score - 5
        )

        target = int(decline)

        rows.append(
            {
                "student_id": student_id,

                "overall_score": overall_score,
                "recent_score": recent_score,
                "previous_score": previous_score,
                "accuracy": accuracy,
                "trend_slope": trend_slope,
                "improvement": improvement,
                "weak_topic_count": weak_topic_count,
                "average_time_taken": average_time_taken,
                "attempt_rate": attempt_rate,

                "target": target,
            }
        )

    return pd.DataFrame(rows)


def train_model():

    print("=" * 60)
    print("TRAINING STUDENT PERFORMANCE RISK MODEL")
    print("=" * 60)

    # -----------------------------------------------------
    # Load data
    # -----------------------------------------------------

    df = load_assessments()

    training_df = create_training_data(
        df
    )

    print(
        f"Training samples: "
        f"{len(training_df)}"
    )

    print(
        "\nTarget distribution:"
    )

    print(
        training_df["target"]
        .value_counts()
    )

    # -----------------------------------------------------
    # Features / target
    # -----------------------------------------------------

    X = training_df[
        FEATURE_COLUMNS
    ]

    y = training_df[
        "target"
    ]

    # -----------------------------------------------------
    # Train / test split
    # -----------------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y,
        )
    )

    # -----------------------------------------------------
    # Random Forest
    # -----------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(
        X_train,
        y_train,
    )

    # -----------------------------------------------------
    # Evaluation
    # -----------------------------------------------------

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    print(
        f"\nAccuracy: "
        f"{accuracy:.3f}"
    )

    # ROC-AUC requires both classes
    if len(
        set(y_test)
    ) > 1:

        auc = roc_auc_score(
            y_test,
            probabilities,
        )

        print(
            f"ROC-AUC: "
            f"{auc:.3f}"
        )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    print(
        "Confusion Matrix:"
    )

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    # -----------------------------------------------------
    # Feature importance
    # -----------------------------------------------------

    importance = pd.Series(
        model.feature_importances_,
        index=FEATURE_COLUMNS,
    ).sort_values(
        ascending=False
    )

    print(
        "\nFeature Importance:"
    )

    print(importance)

    # -----------------------------------------------------
    # Save model
    # -----------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_FILE,
    )

    print(
        f"\nModel saved to: "
        f"{MODEL_FILE}"
    )


if __name__ == "__main__":
    train_model()