"""Health check API router.

Provides a ``GET /health`` endpoint that returns basic status information.
The implementation is intentionally minimal – just to satisfy the requirements
for a simple health probe used by tests and during development.
"""

from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def health() -> dict[str, str]:
    """Return a simple JSON payload indicating the service is healthy.

    Returns
    -------
    dict
        ``{"status": "ok"}``
    """
    return {"status": "ok"}
