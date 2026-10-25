from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DATA_FILE = Path("data/assessments.csv")


REQUIRED_COLUMNS = [
    "student_id",
    "student_name",
    "class_id",
    "subject",
    "topic",
    "assessment_name",
    "marks_obtained",
    "total_marks",
    "attempt_date",
    "time_taken",
    "questions_attempted",
    "questions_correct",
]


# ---------------------------------------------------------
# Validate columns
# ---------------------------------------------------------

def validate_columns(df: pd.DataFrame) -> None:
    """
    Check whether all required columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


# ---------------------------------------------------------
# Validate values
# ---------------------------------------------------------

def validate_values(df: pd.DataFrame) -> None:
    """
    Validate assessment values.
    """

    # Marks cannot be negative
    if (df["marks_obtained"] < 0).any():
        raise ValueError(
            "marks_obtained cannot be negative"
        )

    # Total marks must be positive
    if (df["total_marks"] <= 0).any():
        raise ValueError(
            "total_marks must be greater than zero"
        )

    # Marks cannot exceed total marks
    if (
        df["marks_obtained"]
        > df["total_marks"]
    ).any():
        raise ValueError(
            "marks_obtained cannot exceed total_marks"
        )

    # Questions attempted cannot be negative
    if (
        df["questions_attempted"] < 0
    ).any():
        raise ValueError(
            "questions_attempted cannot be negative"
        )

    # Correct questions cannot be negative
    if (
        df["questions_correct"] < 0
    ).any():
        raise ValueError(
            "questions_correct cannot be negative"
        )

    # Correct questions cannot exceed attempted
    if (
        df["questions_correct"]
        > df["questions_attempted"]
    ).any():
        raise ValueError(
            "questions_correct cannot exceed "
            "questions_attempted"
        )


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

def load_assessments(
    file_path: Path = DATA_FILE,
) -> pd.DataFrame:
    """
    Load and validate assessment data.

    Returns
    -------
    pd.DataFrame
        Cleaned assessment dataset.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    # Read CSV
    df = pd.read_csv(file_path)

    # Validate schema
    validate_columns(df)

    # Convert numeric columns
    numeric_columns = [
        "marks_obtained",
        "total_marks",
        "time_taken",
        "questions_attempted",
        "questions_correct",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Convert date
    df["attempt_date"] = pd.to_datetime(
        df["attempt_date"],
        errors="coerce",
    )

    # Check for invalid numeric/date values
    if df[numeric_columns].isnull().any().any():
        raise ValueError(
            "Dataset contains invalid numeric values"
        )

    if df["attempt_date"].isnull().any():
        raise ValueError(
            "Dataset contains invalid dates"
        )

    # Validate values
    validate_values(df)

    # -----------------------------------------------------
    # Derived metric: score percentage
    # -----------------------------------------------------

    df["score_percentage"] = (
        df["marks_obtained"]
        / df["total_marks"]
        * 100
    )

    # -----------------------------------------------------
    # Derived metric: accuracy
    # -----------------------------------------------------

    df["accuracy"] = 0.0

    valid_attempts = (
        df["questions_attempted"] > 0
    )

    df.loc[valid_attempts, "accuracy"] = (
        df.loc[
            valid_attempts,
            "questions_correct",
        ]
        / df.loc[
            valid_attempts,
            "questions_attempted",
        ]
        * 100
    )

    # Round derived metrics
    df["score_percentage"] = df[
        "score_percentage"
    ].round(2)

    df["accuracy"] = df[
        "accuracy"
    ].round(2)

    # Sort data
    df = df.sort_values(
        by=[
            "student_id",
            "attempt_date",
        ]
    ).reset_index(drop=True)

    return df