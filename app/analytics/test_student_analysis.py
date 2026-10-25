from app.analytics.student_analysis import (
    analyze_student,
)
from app.data.loader import load_assessments


def main():

    df = load_assessments()

    # Select first student
    student_id = (
        df["student_id"]
        .iloc[0]
    )

    result = analyze_student(
        df,
        student_id,
    )

    print("=" * 70)
    print("STUDENT PERFORMANCE ANALYSIS")
    print("=" * 70)

    print(
        f"Student: "
        f"{result['student_name']}"
    )

    print(
        f"Student ID: "
        f"{result['student_id']}"
    )

    print(
        f"Class: "
        f"{result['class_id']}"
    )

    print(
        f"\nOverall Score: "
        f"{result['overall_score']}%"
    )

    print(
        f"Accuracy: "
        f"{result['accuracy']}%"
    )

    print(
        f"Trend: "
        f"{result['trend']}"
    )

    print(
        f"Trend Slope: "
        f"{result['trend_slope']}"
    )

    print(
        f"Improvement: "
        f"{result['improvement']}%"
    )

    print("\nSubject Performance:")

    for subject, score in (
        result[
            "subject_performance"
        ].items()
    ):
        print(
            f"  {subject}: {score}%"
        )

    print("\nTopic Performance:")

    for topic, score in (
        result[
            "topic_performance"
        ].items()
    ):
        print(
            f"  {topic}: {score}%"
        )

    print("\nStrong Topics:")

    for topic in result[
        "strong_topics"
    ]:
        print(
            f"  + {topic}"
        )

    print("\nWeak Topics:")

    for topic in result[
        "weak_topics"
    ]:
        print(
            f"  - {topic}"
        )

    print("\nRecommendation:")

    print(
        result["recommendation"]
    )

    print("\nRecent Assessments:")

    for assessment in result[
        "recent_assessments"
    ]:
        print(
            f"  {assessment['date']} | "
            f"{assessment['assessment_name']} | "
            f"{assessment['score']}%"
        )


if __name__ == "__main__":
    main()