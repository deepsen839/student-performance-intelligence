import pandas as pd

from app.analytics.metrics import (
    calculate_improvement,
    calculate_trend,
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


def build_student_features(
    student_df: pd.DataFrame,
) -> dict:
    """
    Build the feature vector used by the risk model
    for one student.

    The feature definitions must remain consistent
    between training and prediction.
    """

    student_df = (
        student_df
        .sort_values("attempt_date")
        .reset_index(drop=True)
    )

    if len(student_df) < 4:
        raise ValueError(
            "At least 4 assessments are required "
            "for risk prediction."
        )

    # -----------------------------------------------------
    # Overall score
    # -----------------------------------------------------

    overall_score = (
        student_df["score_percentage"]
        .mean()
    )

    # -----------------------------------------------------
    # Recent performance
    # -----------------------------------------------------

    recent_window = min(
        3,
        len(student_df),
    )

    recent_score = (
        student_df
        .tail(recent_window)[
            "score_percentage"
        ]
        .mean()
    )

    # -----------------------------------------------------
    # Previous performance
    # -----------------------------------------------------

    if len(student_df) >= 6:

        previous_score = (
            student_df
            .iloc[-6:-3][
                "score_percentage"
            ]
            .mean()
        )

    else:

        midpoint = len(student_df) // 2

        previous_score = (
            student_df
            .iloc[:midpoint][
                "score_percentage"
            ]
            .mean()
        )

    # -----------------------------------------------------
    # Accuracy
    # -----------------------------------------------------

    total_attempted = (
        student_df[
            "questions_attempted"
        ].sum()
    )

    total_correct = (
        student_df[
            "questions_correct"
        ].sum()
    )

    if total_attempted > 0:

        accuracy = (
            total_correct
            / total_attempted
            * 100
        )

    else:
        accuracy = 0.0

    # -----------------------------------------------------
    # Trend
    # -----------------------------------------------------

    trend_result = calculate_trend(
        student_df
    )

    trend_slope = trend_result[
        "slope"
    ]

    # -----------------------------------------------------
    # Improvement
    # -----------------------------------------------------

    improvement = calculate_improvement(
        student_df
    )

    # -----------------------------------------------------
    # Weak topics
    # -----------------------------------------------------

    topic_scores = (
        student_df
        .groupby("topic")[
            "score_percentage"
        ]
        .mean()
    )

    weak_topic_count = int(
        (topic_scores < 50).sum()
    )

    # -----------------------------------------------------
    # Average time
    # -----------------------------------------------------

    average_time_taken = (
        student_df["time_taken"]
        .mean()
    )

    # -----------------------------------------------------
    # Attempt rate
    # -----------------------------------------------------

    total_questions_available = (
        len(student_df) * 30
    )

    attempt_rate = (
        student_df[
            "questions_attempted"
        ].sum()
        / total_questions_available
        * 100
    )

    # -----------------------------------------------------
    # Return features
    # -----------------------------------------------------

    return {
        "overall_score": round(
            overall_score,
            2,
        ),
        "recent_score": round(
            recent_score,
            2,
        ),
        "previous_score": round(
            previous_score,
            2,
        ),
        "accuracy": round(
            accuracy,
            2,
        ),
        "trend_slope": round(
            trend_slope,
            2,
        ),
        "improvement": round(
            improvement,
            2,
        ),
        "weak_topic_count": (
            weak_topic_count
        ),
        "average_time_taken": round(
            average_time_taken,
            2,
        ),
        "attempt_rate": round(
            attempt_rate,
            2,
        ),
    }