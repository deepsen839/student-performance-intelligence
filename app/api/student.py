from fastapi import APIRouter, HTTPException

from app.analytics.student_analysis import (
    analyze_student,
)
from app.models.schemas import (
    StudentInsightsResponse,
    StudentTrendResponse,
)


router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@router.get(
    "/{student_id}/insights",
    response_model=StudentInsightsResponse,
)
def get_student_insights(
    student_id: str,
):
    """
    Return complete performance intelligence
    for a student.
    """

    from app.main import assessment_df

    try:

        result = analyze_student(
            assessment_df,
            student_id,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/{student_id}/trend",
    response_model=StudentTrendResponse,
)
def get_student_trend(
    student_id: str,
):
    """
    Return performance trend for a student.
    """

    from app.main import assessment_df

    try:

        result = analyze_student(
            assessment_df,
            student_id,
        )

        return {
            "student_id": student_id,
            "trend": result["trend"],
            "trend_slope": result[
                "trend_slope"
            ],
            "improvement": result[
                "improvement"
            ],
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )