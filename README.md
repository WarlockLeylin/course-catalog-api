# Course Catalog API

A standalone backend project built with FastAPI and Pydantic for managing a course catalog.

## Description
This project implements a RESTful API for a university course catalog. It supports retrieving course lists with filtering, title search, sorting, validated pagination, individual course detail lookup, and summary statistics.

## How to Run

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\Activate.ps1  # Windows
   ```

2. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```

3. Run development server:
    ```bash
   fastapi dev main.py
   ```

4. API documentation:
- Open http://127.0.0.1:8000/docs (Swagger UI)
- Open http://127.0.0.1:8000/redoc (ReDoc)

## What Was Verified

### Base Requirements
| Request Path | Expected Result / Response Summary |
| :--- | :--- |
| `GET /` | `{"message": "Course Catalog API is running"}` |
| `GET /courses` | 6 courses; `ai-integration` first (32 likes), `api-design` last (11). |
| `GET /courses?is_elective=true` | 2 courses: `ai-integration`, `api-design`. |
| `GET /courses?is_elective=false` | 4 courses: `modern-frontend`, `web-security`, `backend-fastapi`, `databases-postgresql`. |
| `GET /courses?sort=title` | 6 courses alphabetically by title (`ai-integration` ... `web-security`). |
| `GET /courses?page=1&page_size=2` | `ai-integration`, `modern-frontend`. |
| `GET /courses?page=2&page_size=2` | `web-security`, `backend-fastapi`. |
| `GET /courses?page=3&page_size=2` | `databases-postgresql`, `api-design`. |
| `GET /courses?page=4&page_size=2` | Empty list `[]`. |
| `GET /courses/web-security` | Returns details for *Web Security Essentials*. |
| `GET /courses/nope` | Returns `404 Not Found` with `{"detail": "Course not found"}`. |

---

### Bonus Features Completed

1. **Strict Sort Validation (`Literal["popular", "title"]`)**:
   - `GET /courses?sort=banana` returns `422 Unprocessable Entity` (invalid query param).
   - `/docs` displays a dropdown menu for `sort`.

2. **Protected Pagination (`Query` constraints with `Annotated`)**:
   - `page` must be >= 1, `page_size` must be between 1 and 100.
   - `GET /courses?page=0&page_size=1000` returns `422 Unprocessable Entity`.

3. **Title Substring Search (`q` parameter)**:
   - `GET /courses?q=react` returns `modern-frontend`.
   - `GET /courses?q=api` returns `backend-fastapi` and `api-design`.

4. **Statistics Endpoint (`GET /stats`)**:
   - `GET /stats` returns `{"total": 6, "total_credits": 28, "electives": 2}` via `Stats` Pydantic model.