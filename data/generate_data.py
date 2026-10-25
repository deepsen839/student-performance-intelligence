import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


random.seed(42)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

NUM_STUDENTS = 60
NUM_ASSESSMENTS = 10

OUTPUT_FILE = Path("data/assessments.csv")


SUBJECT_TOPICS = {
    "Physics": [
        "Mechanics",
        "Current Electricity",
        "Electromagnetism",
        "Optics",
        "Thermodynamics",
    ],
    "Mathematics": [
        "Algebra",
        "Calculus",
        "Probability",
        "Trigonometry",
        "Geometry",
    ],
    "Chemistry": [
        "Organic Chemistry",
        "Chemical Bonding",
        "Thermodynamics",
        "Equilibrium",
        "Electrochemistry",
    ],
}


FIRST_NAMES = [
    "Rahul",
    "Amit",
    "Rohan",
    "Arjun",
    "Vikram",
    "Karan",
    "Aditya",
    "Ankit",
    "Sahil",
    "Ravi",
    "Priya",
    "Neha",
    "Ananya",
    "Sneha",
    "Pooja",
    "Riya",
    "Kavya",
    "Simran",
    "Isha",
    "Aditi",
]


# ---------------------------------------------------------
# Student generation
# ---------------------------------------------------------

def generate_students():
    students = []

    for i in range(NUM_STUDENTS):
        student_id = f"S{i + 1:03d}"

        first_name = FIRST_NAMES[i % len(FIRST_NAMES)]

        # Make names unique
        if i >= len(FIRST_NAMES):
            first_name = f"{first_name}_{i // len(FIRST_NAMES) + 1}"

        class_id = random.choice(
            ["10-A", "10-B", "10-C"]
        )

        # Base ability of the student
        base_ability = random.uniform(50, 85)

        # Create different performance patterns
        pattern = random.choice(
            [
                "improving",
                "declining",
                "stable",
            ]
        )

        students.append(
            {
                "student_id": student_id,
                "student_name": first_name,
                "class_id": class_id,
                "base_ability": base_ability,
                "pattern": pattern,
            }
        )

    return students


# ---------------------------------------------------------
# Generate one assessment
# ---------------------------------------------------------

def generate_assessment(
    student,
    assessment_number,
    subject,
    topic,
    attempt_date,
):
    base_score = student["base_ability"]

    # Introduce performance trend
    if student["pattern"] == "improving":
        trend_effect = assessment_number * 2.0

    elif student["pattern"] == "declining":
        trend_effect = -assessment_number * 2.0

    else:
        trend_effect = random.uniform(-2, 2)

    # Topic-specific variation
    topic_effect = random.uniform(-12, 12)

    score = (
        base_score
        + trend_effect
        + topic_effect
        + random.gauss(0, 5)
    )

    # Keep score realistic
    score = max(20, min(98, score))

    total_marks = 100
    marks_obtained = round(score)

    # Number of questions
    total_questions = 30

    questions_attempted = random.randint(
        20,
        total_questions,
    )

    # Accuracy roughly follows performance
    accuracy = score / 100

    questions_correct = round(
        questions_attempted * accuracy
        + random.gauss(0, 1.5)
    )

    questions_correct = max(
        0,
        min(
            questions_attempted,
            questions_correct,
        ),
    )

    # Time taken in minutes
    time_taken = random.randint(25, 60)

    assessment_name = f"Test {assessment_number}"

    return {
        "student_id": student["student_id"],
        "student_name": student["student_name"],
        "class_id": student["class_id"],
        "subject": subject,
        "topic": topic,
        "assessment_name": assessment_name,
        "marks_obtained": marks_obtained,
        "total_marks": total_marks,
        "attempt_date": attempt_date.strftime("%Y-%m-%d"),
        "time_taken": time_taken,
        "questions_attempted": questions_attempted,
        "questions_correct": questions_correct,
    }


# ---------------------------------------------------------
# Generate complete dataset
# ---------------------------------------------------------

def generate_dataset():
    students = generate_students()

    records = []

    start_date = datetime(2026, 6, 1)

    for student in students:

        for assessment_number in range(
            1,
            NUM_ASSESSMENTS + 1,
        ):

            # Select subject
            subject = random.choice(
                list(SUBJECT_TOPICS.keys())
            )

            # Select topic from that subject
            topic = random.choice(
                SUBJECT_TOPICS[subject]
            )

            attempt_date = (
                start_date
                + timedelta(
                    days=(assessment_number - 1) * 7
                )
            )

            record = generate_assessment(
                student=student,
                assessment_number=assessment_number,
                subject=subject,
                topic=topic,
                attempt_date=attempt_date,
            )

            records.append(record)

    df = pd.DataFrame(records)

    # Sort by student and date
    df = df.sort_values(
        by=[
            "student_id",
            "attempt_date",
        ]
    )

    return df


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = generate_dataset()

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 60)
    print("Dataset generated successfully")
    print("=" * 60)

    print(f"File: {OUTPUT_FILE}")
    print(f"Records: {len(df)}")
    print(f"Students: {df['student_id'].nunique()}")
    print(f"Subjects: {df['subject'].nunique()}")
    print(f"Topics: {df['topic'].nunique()}")
    print(
        f"Assessments per student: "
        f"{len(df) // df['student_id'].nunique()}"
    )

    print("\nSubjects:")
    print(df["subject"].value_counts())

    print("\nSample records:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()