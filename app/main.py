from fastapi import FastAPI

from app.api.class_analysis import (
    router as class_router,
)
from app.api.student import (
    router as student_router,
)
from app.data.loader import (
    load_assessments,
)


# ---------------------------------------------------------
# Load data once when the application starts
# ---------------------------------------------------------

assessment_df = load_assessments()


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Student Performance Intelligence System",
    description=(
        "AI-powered student performance "
        "analysis and intelligence API"
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Register routers
# ---------------------------------------------------------

app.include_router(
    student_router
)

app.include_router(
    class_router
)


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get(
    "/health",
    tags=["System"],
)
def health_check():

    return {
        "status": "healthy",
        "service": (
            "student-performance-intelligence"
        ),
        "records_loaded": len(
            assessment_df
        ),
    }