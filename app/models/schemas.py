from typing import Any

from pydantic import BaseModel, Field


class StudentInsightsResponse(BaseModel):
    student_id: str
    student_name: str
    class_id: str

    overall_score: float = Field(
        ge=0,
        le=100,
    )

    accuracy: float = Field(
        ge=0,
        le=100,
    )

    subject_performance: dict[str, float]
    topic_performance: dict[str, float]

    strong_topics: list[str]
    weak_topics: list[str]

    trend: str
    trend_slope: float
    improvement: float

    recommendation: str

    recent_assessments: list[dict[str, Any]]


class StudentTrendResponse(BaseModel):
    student_id: str
    trend: str
    trend_slope: float
    improvement: float
    risk_score: float | None = None
    risk_level: str | None = None
    risk_factors: list[str] = []


class ClassInsightsResponse(BaseModel):
    class_id: str

    class_average: float

    subject_averages: dict[str, float]
    topic_averages: dict[str, float]

    strongest_topic: str | None
    weakest_topic: str | None
    weakest_topic_score: float

    student_counts: dict[str, int]

    improving_students: list[dict[str, Any]]
    declining_students: list[dict[str, Any]]
    stable_students: list[dict[str, Any]]

    students_requiring_attention: list[
        dict[str, Any]
    ]

    recommendation: str


class StudentsAtRiskResponse(BaseModel):
    class_id: str
    total_students_requiring_attention: int
    students: list[dict[str, Any]]