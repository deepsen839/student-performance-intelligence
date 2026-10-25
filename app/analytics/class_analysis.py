import pandas as pd

from app.analytics.student_analysis import analyze_student


def calculate_class_average(
    class_df: pd.DataFrame,
) -> float:
    """
    Calculate average score for the entire class.
    """

    if class_df.empty:
        return 0.0

    return round(
        class_df["score_percentage"].mean(),
        2,
    )


def calculate_subject_averages(
    class_df: pd.DataFrame,
) -> dict:
    """
    Calculate average score for each subject.
    """

    return (
        class_df
        .groupby("subject")["score_percentage"]
        .mean()
        .round(2)
        .to_dict()
    )


def calculate_topic_averages(
    class_df: pd.DataFrame,
) -> dict:
    """
    Calculate average score for each topic.
    """

    return (
        class_df
        .groupby("topic")["score_percentage"]
        .mean()
        .round(2)
        .to_dict()
    )


def identify_strongest_topic(
    topic_averages: dict,
):
    """
    Return the strongest topic.
    """

    if not topic_averages:
        return None

    return max(
        topic_averages,
        key=topic_averages.get,
    )


def identify_weakest_topic(
    topic_averages: dict,
):
    """
    Return the weakest topic.
    """

    if not topic_averages:
        return None

    return min(
        topic_averages,
        key=topic_averages.get,
    )


def classify_students(
    class_df: pd.DataFrame,
) -> dict:
    """
    Analyze every student in the class and
    classify them as improving, declining,
    or stable.
    """

    student_results = []

    for student_id in (
        class_df["student_id"]
        .unique()
    ):

        try:
            result = analyze_student(
                class_df,
                student_id,
            )

            student_results.append(result)

        except ValueError:
            continue

    improving = []
    declining = []
    stable = []

    for result in student_results:

        student_summary = {
            "student_id": result[
                "student_id"
            ],
            "student_name": result[
                "student_name"
            ],
            "overall_score": result[
                "overall_score"
            ],
            "accuracy": result[
                "accuracy"
            ],
            "trend": result[
                "trend"
            ],
            "improvement": result[
                "improvement"
            ],
            "weak_topics": result[
                "weak_topics"
            ],
        }

        if result["trend"] == "improving":
            improving.append(
                student_summary
            )

        elif result["trend"] == "declining":
            declining.append(
                student_summary
            )

        else:
            stable.append(
                student_summary
            )

    return {
        "improving": improving,
        "declining": declining,
        "stable": stable,
        "all_students": student_results,
    }


def identify_students_requiring_attention(
    student_results: list,
) -> list:
    """
    Identify students requiring additional attention.

    A student is flagged when:
      - performance is declining, OR
      - overall score is below 50%, OR
      - improvement is strongly negative.

    Students are ranked by severity.
    """

    attention_students = []

    for result in student_results:

        score = result[
            "overall_score"
        ]

        trend = result[
            "trend"
        ]

        improvement = result[
            "improvement"
        ]

        reasons = []

        severity = 0

        # Low overall performance
        if score < 50:
            severity += 3
            reasons.append(
                "Low overall performance"
            )

        elif score < 60:
            severity += 1
            reasons.append(
                "Below-average performance"
            )

        # Declining trend
        if trend == "declining":
            severity += 3
            reasons.append(
                "Performance is declining"
            )

        # Significant recent decline
        if improvement <= -5:
            severity += 2
            reasons.append(
                "Recent performance has declined"
            )

        # Weak topics
        if len(
            result["weak_topics"]
        ) >= 2:
            severity += 1
            reasons.append(
                "Multiple weak topics"
            )

        if severity > 0:

            attention_students.append(
                {
                    "student_id": result[
                        "student_id"
                    ],
                    "student_name": result[
                        "student_name"
                    ],
                    "overall_score": score,
                    "trend": trend,
                    "improvement": improvement,
                    "weak_topics": result[
                        "weak_topics"
                    ],
                    "severity": severity,
                    "reasons": reasons,
                }
            )

    # Highest severity first
    attention_students.sort(
        key=lambda x: (
            x["severity"],
            -x["overall_score"],
        ),
        reverse=True,
    )

    return attention_students


def generate_class_recommendation(
    weakest_topic: str,
    weakest_topic_score: float,
    declining_count: int,
    class_average: float,
) -> str:
    """
    Generate a simple deterministic recommendation
    for the teacher.
    """

    if weakest_topic is None:
        return (
            "Continue monitoring class performance "
            "and maintain regular assessments."
        )

    if weakest_topic_score < 50:

        return (
            f"Conduct a revision session on "
            f"{weakest_topic}. The class average "
            f"for this topic is only "
            f"{weakest_topic_score:.1f}%."
        )

    if declining_count > 0:

        return (
            f"Review {weakest_topic} and provide "
            "targeted practice to students showing "
            "a declining trend."
        )

    if class_average < 60:

        return (
            "Consider additional revision sessions "
            "and targeted practice across the class."
        )

    return (
        f"Continue regular practice while "
        f"reinforcing {weakest_topic}."
    )


def analyze_class(
    df: pd.DataFrame,
    class_id: str,
) -> dict:
    """
    Generate complete performance intelligence
    for a class.
    """

    # -----------------------------------------------------
    # Filter class
    # -----------------------------------------------------

    class_df = df[
        df["class_id"] == class_id
    ].copy()

    if class_df.empty:
        raise ValueError(
            f"Class not found: {class_id}"
        )

    # -----------------------------------------------------
    # Basic metrics
    # -----------------------------------------------------

    class_average = calculate_class_average(
        class_df
    )

    subject_averages = (
        calculate_subject_averages(
            class_df
        )
    )

    topic_averages = (
        calculate_topic_averages(
            class_df
        )
    )

    strongest_topic = (
        identify_strongest_topic(
            topic_averages
        )
    )

    weakest_topic = (
        identify_weakest_topic(
            topic_averages
        )
    )

    # -----------------------------------------------------
    # Student classification
    # -----------------------------------------------------

    student_classification = classify_students(
        class_df
    )

    improving_students = (
        student_classification[
            "improving"
        ]
    )

    declining_students = (
        student_classification[
            "declining"
        ]
    )

    stable_students = (
        student_classification[
            "stable"
        ]
    )

    all_students = (
        student_classification[
            "all_students"
        ]
    )

    # -----------------------------------------------------
    # Students requiring attention
    # -----------------------------------------------------

    attention_students = (
        identify_students_requiring_attention(
            all_students
        )
    )

    # -----------------------------------------------------
    # Weakest topic score
    # -----------------------------------------------------

    weakest_topic_score = 0.0

    if weakest_topic is not None:
        weakest_topic_score = topic_averages[
            weakest_topic
        ]

    # -----------------------------------------------------
    # Recommendation
    # -----------------------------------------------------

    recommendation = (
        generate_class_recommendation(
            weakest_topic=weakest_topic,
            weakest_topic_score=weakest_topic_score,
            declining_count=len(
                declining_students
            ),
            class_average=class_average,
        )
    )

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return {
        "class_id": class_id,

        "class_average": class_average,

        "subject_averages": (
            subject_averages
        ),

        "topic_averages": (
            topic_averages
        ),

        "strongest_topic": (
            strongest_topic
        ),

        "weakest_topic": (
            weakest_topic
        ),

        "weakest_topic_score": (
            weakest_topic_score
        ),

        "student_counts": {
            "total": len(all_students),
            "improving": len(
                improving_students
            ),
            "declining": len(
                declining_students
            ),
            "stable": len(
                stable_students
            ),
        },

        "improving_students": (
            improving_students
        ),

        "declining_students": (
            declining_students
        ),

        "stable_students": stable_students,

        "students_requiring_attention": (
            attention_students
        ),

        "recommendation": recommendation,
    }