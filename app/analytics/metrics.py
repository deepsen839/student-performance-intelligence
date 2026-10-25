import pandas as pd
from sklearn.linear_model import LinearRegression


def calculate_overall_score(
    student_df: pd.DataFrame,
) -> float:
    """
    Calculate the student's average score percentage.
    """

    if student_df.empty:
        return 0.0

    return round(
        student_df["score_percentage"].mean(),
        2,
    )


def calculate_accuracy(
    student_df: pd.DataFrame,
) -> float:
    """
    Calculate overall question accuracy.

    We calculate accuracy from total questions rather
    than averaging individual assessment accuracies.
    """

    total_attempted = student_df[
        "questions_attempted"
    ].sum()

    total_correct = student_df[
        "questions_correct"
    ].sum()

    if total_attempted == 0:
        return 0.0

    accuracy = (
        total_correct
        / total_attempted
        * 100
    )

    return round(accuracy, 2)


def calculate_subject_performance(
    student_df: pd.DataFrame,
) -> dict:
    """
    Calculate average performance for each subject.
    """

    result = (
        student_df
        .groupby("subject")["score_percentage"]
        .mean()
        .round(2)
        .to_dict()
    )

    return result


def calculate_topic_performance(
    student_df: pd.DataFrame,
) -> dict:
    """
    Calculate average performance for each topic.
    """

    result = (
        student_df
        .groupby("topic")["score_percentage"]
        .mean()
        .round(2)
        .to_dict()
    )

    return result


def identify_strong_topics(
    topic_scores: dict,
    threshold: float = 75.0,
) -> list:
    """
    Topics with average score >= threshold
    are considered strong.
    """

    strong_topics = [
        topic
        for topic, score in topic_scores.items()
        if score >= threshold
    ]

    # Sort strongest first
    strong_topics.sort(
        key=lambda topic: topic_scores[topic],
        reverse=True,
    )

    return strong_topics


def identify_weak_topics(
    topic_scores: dict,
    threshold: float = 50.0,
) -> list:
    """
    Topics with average score < threshold
    are considered weak.
    """

    weak_topics = [
        topic
        for topic, score in topic_scores.items()
        if score < threshold
    ]

    # Sort weakest first
    weak_topics.sort(
        key=lambda topic: topic_scores[topic],
    )

    return weak_topics


def calculate_trend(
    student_df: pd.DataFrame,
    stable_threshold: float = 1.0,
) -> dict:
    """
    Calculate performance trend using linear regression.

    Positive slope  -> improving
    Negative slope  -> declining
    Near zero       -> stable
    """

    if len(student_df) < 2:
        return {
            "trend": "insufficient_data",
            "slope": 0.0,
        }

    # Ensure chronological order
    df = student_df.sort_values(
        "attempt_date"
    ).reset_index(drop=True)

    # Assessment sequence
    X = (
        df.index.values
        .reshape(-1, 1)
    )

    # Scores
    y = df[
        "score_percentage"
    ].values

    model = LinearRegression()

    model.fit(X, y)

    slope = float(
        model.coef_[0]
    )

    if slope > stable_threshold:
        trend = "improving"

    elif slope < -stable_threshold:
        trend = "declining"

    else:
        trend = "stable"

    return {
        "trend": trend,
        "slope": round(slope, 2),
    }


def calculate_improvement(
    student_df: pd.DataFrame,
    window: int = 3,
) -> float:
    """
    Compare the recent average with the previous
    average.

    Positive value -> improvement
    Negative value -> decline
    """

    df = student_df.sort_values(
        "attempt_date"
    )

    if len(df) < 2:
        return 0.0

    # If enough assessments exist, compare
    # recent N against previous N.
    if len(df) >= window * 2:

        previous = df.iloc[
            -window * 2:-window
        ]["score_percentage"].mean()

        recent = df.iloc[
            -window:
        ]["score_percentage"].mean()

    else:

        midpoint = len(df) // 2

        previous = df.iloc[
            :midpoint
        ]["score_percentage"].mean()

        recent = df.iloc[
            midpoint:
        ]["score_percentage"].mean()

    improvement = recent - previous

    return round(
        improvement,
        2,
    )


def calculate_recommendation(
    weak_topics: list,
    trend: str,
    improvement: float,
) -> str:
    """
    Generate a deterministic recommendation
    from the analytical results.
    """

    if weak_topics:
        topics = ", ".join(
            weak_topics[:2]
        )

        if trend == "declining":
            return (
                f"Focus on {topics} and complete "
                "additional practice assessments "
                "to reverse the recent decline."
            )

        return (
            f"Focus on {topics} through targeted "
            "practice and revision."
        )

    if trend == "declining":
        return (
            "Review recent assessments and "
            "increase targeted practice."
        )

    if improvement > 5:
        return (
            "Continue the current study strategy "
            "and gradually increase assessment "
            "difficulty."
        )

    return (
        "Maintain consistent practice and "
        "monitor performance across upcoming "
        "assessments."
    )