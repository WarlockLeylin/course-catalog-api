from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Query

from data import find_course, get_all_courses
from models import Course, Stats

app = FastAPI(title="Course Catalog API")


# Pagination dependency with Query parameter validation
def pagination(
    page: Annotated[int, Query(ge=1, description="Page number, starting from 1")] = 1,
    page_size: Annotated[
        int, Query(ge=1, le=100, description="Items per page (1-100)")
    ] = 20) -> dict[str, int]:
    offset = (page - 1) * page_size
    return {"offset": offset, "limit": page_size}


@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


# GET /stats endpoint returning total courses, total credits, and electives count
@app.get("/stats", response_model=Stats)
def get_stats():
    courses = get_all_courses()
    total = len(courses)
    total_credits = sum(c.credits for c in courses)
    electives = sum(1 for c in courses if c.is_elective)
    return Stats(
        total=total,
        total_credits=total_credits,
        electives=electives,
    )


@app.get("/courses", response_model=list[Course])
def list_courses(
    is_elective: bool | None = None,
    # Strict validation for sort parameter using Literal
    sort: Literal["popular", "title"] = "popular",
    # Substring search query parameter
    q: str | None = None,
    p: dict = Depends(pagination),
):
    courses = get_all_courses()

    # Filter by search query q (case-insensitive substring match)
    if q is not None:
        courses = [c for c in courses if q.lower() in c.title.lower()]

    # Filter by elective status
    if is_elective is not None:
        courses = [c for c in courses if c.is_elective == is_elective]

    # Apply sorting
    if sort == "title":
        courses = sorted(courses, key=lambda c: c.title)
    else:
        # Default: sort by popularity (likes descending)
        courses = sorted(courses, key=lambda c: c.likes, reverse=True)

    # Apply pagination slicing
    offset = p["offset"]
    limit = p["limit"]
    return courses[offset : offset + limit]


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = find_course(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course