def generate_risk_factors(
    feature_row: dict,
) -> list[str]:
    """
    Generate human-readable explanations for
    the model risk prediction.

    These are rule-based explanations of the
    model input features.
    """

    factors = []

    if feature_row[
        "trend_slope"
    ] < -1:

        factors.append(
            "Performance trend is declining"
        )

    if feature_row[
        "improvement"
    ] <= -5:

        factors.append(
            "Recent performance has declined"
        )

    if feature_row[
        "recent_score"
    ] < 50:

        factors.append(
            "Recent assessment scores are low"
        )

    if feature_row[
        "accuracy"
    ] < 60:

        factors.append(
            "Question accuracy is low"
        )

    if feature_row[
        "weak_topic_count"
    ] >= 2:

        factors.append(
            "Multiple topics require improvement"
        )

    if feature_row[
        "attempt_rate"
    ] < 70:

        factors.append(
            "Question attempt rate is low"
        )

    if not factors:

        factors.append(
            "No major negative performance "
            "signals were detected"
        )

    return factors