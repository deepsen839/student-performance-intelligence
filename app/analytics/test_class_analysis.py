from app.analytics.class_analysis import (
    analyze_class,
)
from app.data.loader import load_assessments


def main():

    df = load_assessments()

    # Select first class
    class_id = (
        df["class_id"]
        .iloc[0]
    )

    result = analyze_class(
        df,
        class_id,
    )

    print("=" * 70)
    print("CLASS PERFORMANCE ANALYSIS")
    print("=" * 70)

    print(
        f"Class: {result['class_id']}"
    )

    print(
        f"\nClass Average: "
        f"{result['class_average']}%"
    )

    print("\nSubject Averages:")

    for subject, score in (
        result[
            "subject_averages"
        ].items()
    ):
        print(
            f"  {subject}: {score}%"
        )

    print(
        f"\nStrongest Topic: "
        f"{result['strongest_topic']}"
    )

    print(
        f"Weakest Topic: "
        f"{result['weakest_topic']}"
    )

    print(
        f"Weakest Topic Score: "
        f"{result['weakest_topic_score']}%"
    )

    print("\nStudent Counts:")

    counts = result[
        "student_counts"
    ]

    print(
        f"  Total: {counts['total']}"
    )

    print(
        f"  Improving: "
        f"{counts['improving']}"
    )

    print(
        f"  Declining: "
        f"{counts['declining']}"
    )

    print(
        f"  Stable: "
        f"{counts['stable']}"
    )

    print(
        "\nStudents Requiring Attention:"
    )

    for student in result[
        "students_requiring_attention"
    ][:10]:

        print(
            f"  {student['student_id']} - "
            f"{student['student_name']} | "
            f"Score: "
            f"{student['overall_score']}% | "
            f"Trend: "
            f"{student['trend']} | "
            f"Severity: "
            f"{student['severity']}"
        )

        print(
            f"    Reasons: "
            f"{', '.join(student['reasons'])}"
        )

    print(
        "\nClass Recommendation:"
    )

    print(
        result["recommendation"]
    )


if __name__ == "__main__":
    main()