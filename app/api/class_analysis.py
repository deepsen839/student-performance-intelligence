from fastapi import APIRouter, HTTPException

from app.analytics.class_analysis import (
    analyze_class,
)
from app.models.schemas import (
    ClassInsightsResponse,
    StudentsAtRiskResponse,
)


router = APIRouter(
    prefix="/class",
    tags=["Class"],
)


@router.get(
    "/{class_id}/insights",
    response_model=ClassInsightsResponse,
)
def get_class_insights(
    class_id: str,
):
    """
    Return complete performance intelligence
    for a class.
    """

    from app.main import assessment_df

    try:

        result = analyze_class(
            assessment_df,
            class_id,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/{class_id}/students-at-risk",
    response_model=StudentsAtRiskResponse,
)
def get_students_at_risk(
    class_id: str,
):
    """
    Return students requiring attention.
    """

    from app.main import assessment_df

    try:

        result = analyze_class(
            assessment_df,
            class_id,
        )

        students = result[
            "students_requiring_attention"
        ]

        return {
            "class_id": class_id,
            "total_students_requiring_attention": (
                len(students)
            ),
            "students": students,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )