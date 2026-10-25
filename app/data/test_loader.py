from app.data.loader import load_assessments


def main():
    df = load_assessments()

    print("=" * 60)
    print("DATA LOADER TEST")
    print("=" * 60)

    print(f"Records: {len(df)}")
    print(
        f"Students: {df['student_id'].nunique()}"
    )
    print(
        f"Subjects: {df['subject'].nunique()}"
    )
    print(
        f"Topics: {df['topic'].nunique()}"
    )

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nSample:")
    print(
        df[
            [
                "student_id",
                "subject",
                "topic",
                "marks_obtained",
                "score_percentage",
                "questions_attempted",
                "questions_correct",
                "accuracy",
            ]
        ].head(10).to_string(index=False)
    )

    print("\nAverage score:")
    print(
        round(
            df["score_percentage"].mean(),
            2,
        )
    )

    print("\nAverage accuracy:")
    print(
        round(
            df["accuracy"].mean(),
            2,
        )
    )


if __name__ == "__main__":
    main()