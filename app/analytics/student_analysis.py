import pandas as pd

from app.analytics.metrics import (
    calculate_accuracy,
    calculate_improvement,
    calculate_overall_score,
    calculate_recommendation,
    calculate_subject_performance,
    calculate_topic_performance,
    calculate_trend,
    identify_strong_topics,
    identify_weak_topics,
)
from app.ml.predict import (
    predict_student_risk,
)

from app.ml.explanation import (
    generate_risk_factors,
)

def analyze_student(
    df: pd.DataFrame,
    student_id: str,
) -> dict:
    """
    Generate complete performance intelligence
    for one student.
    """

    # -----------------------------------------------------
    # Filter student
    # -----------------------------------------------------

    student_df = df[
        df["student_id"] == student_id
    ].copy()

    if student_df.empty:
        raise ValueError(
            f"Student not found: {student_id}"
        )

    # -----------------------------------------------------
    # Basic information
    # -----------------------------------------------------

    student_name = student_df[
        "student_name"
    ].iloc[0]

    class_id = student_df[
        "class_id"
    ].iloc[0]

    # -----------------------------------------------------
    # Core metrics
    # -----------------------------------------------------

    overall_score = calculate_overall_score(
        student_df
    )

    accuracy = calculate_accuracy(
        student_df
    )

    # -----------------------------------------------------
    # Subject analysis
    # -----------------------------------------------------

    subject_performance = (
        calculate_subject_performance(
            student_df
        )
    )

    # -----------------------------------------------------
    # Topic analysis
    # -----------------------------------------------------

    topic_performance = (
        calculate_topic_performance(
            student_df
        )
    )

    strong_topics = identify_strong_topics(
        topic_performance
    )

    weak_topics = identify_weak_topics(
        topic_performance
    )

    # -----------------------------------------------------
    # Trend analysis
    # -----------------------------------------------------

    trend_result = calculate_trend(
        student_df
    )

    trend = trend_result["trend"]
    trend_slope = trend_result["slope"]

    # -----------------------------------------------------
    # Improvement
    # -----------------------------------------------------

    improvement = calculate_improvement(
        student_df
    )

    # -----------------------------------------------------
    # Recommendation
    # -----------------------------------------------------

    recommendation = (
        calculate_recommendation(
            weak_topics=weak_topics,
            trend=trend,
            improvement=improvement,
        )
    )

    # -----------------------------------------------------
    # Recent assessments
    # -----------------------------------------------------

    recent_assessments = (
        student_df
        .sort_values("attempt_date")
        .tail(5)
    )

    recent_scores = []

    for _, row in recent_assessments.iterrows():

        recent_scores.append(
            {
                "assessment_name": row[
                    "assessment_name"
                ],
                "subject": row[
                    "subject"
                ],
                "topic": row[
                    "topic"
                ],
                "score": float(
                    row[
                        "score_percentage"
                    ]
                ),
                "accuracy": float(
                    row["accuracy"]
                ),
                "date": row[
                    "attempt_date"
                ].strftime(
                    "%Y-%m-%d"
                ),
            }
        )

    # -----------------------------------------------------
    # Final structured result
    # -----------------------------------------------------
        # -----------------------------------------------------
    # ML risk prediction
    # -----------------------------------------------------

    risk_prediction = None

    try:

        risk_prediction = (
            predict_student_risk(
                df,
                student_id,
            )
        )

        risk_factors = (
            generate_risk_factors(
                risk_prediction[
                    "features"
                ]
            )
        )

    except (
        FileNotFoundError,
        ValueError,
    ):

        # Allow analytics to work even if the
        # ML model has not been trained yet.
        risk_factors = []



    result = {
        "student_id": student_id,
        "student_name": student_name,
        "class_id": class_id,

        "overall_score": overall_score,
        "accuracy": accuracy,

        "subject_performance": (
            subject_performance
        ),

        "topic_performance": (
            topic_performance
        ),

        "strong_topics": strong_topics,
        "weak_topics": weak_topics,

        "trend": trend,
        "trend_slope": trend_slope,
        "improvement": improvement,

        "recommendation": recommendation,

        "recent_assessments": recent_scores,


                "risk_score": (
            risk_prediction["risk_score"]
            if risk_prediction
            else None
        ),

        "risk_level": (
            risk_prediction["risk_level"]
            if risk_prediction
            else None
        ),

        "risk_factors": risk_factors,
    }

    return result