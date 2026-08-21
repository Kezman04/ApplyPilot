from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import ValidationError

from ..schemas.resume_match_schema import ResumeMatchRequest, ResumeMatchResponse
from ..services.resume_matcher import analyze_resume_match, tailor_resume
from ..services.resume_parser import extract_resume_text
from ..schemas.resume_tailor_schema import ResumeTailorRequest, ResumeTailorResponse


router = APIRouter()


@router.post(
    "/api/resume/match",
    status_code=status.HTTP_200_OK,
    response_model=ResumeMatchResponse,
)
def resume_match(request: ResumeMatchRequest) -> ResumeMatchResponse:
    result = analyze_resume_match(
        request.resume_text,
        request.job_description,
    )

    try:
        response = ResumeMatchResponse(**result)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid resume match result: {exc}",
        ) from exc

    return response


@router.post("/api/resume/extract")
async def extract_resume(file: UploadFile = File(...)):
    filename = file.filename or ""
    filename_lower = filename.lower()

    allowed_extensions = (".txt", ".pdf", ".docx")

    if not filename_lower.endswith(allowed_extensions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload a TXT, PDF, or DOCX file.",
        )

    content = await file.read()

    max_file_size = 5 * 1024 * 1024  # 5 MB

    if len(content) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large. Maximum size is 5 MB.",
        )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty.",
        )

    try:
        text = extract_resume_text(filename, content)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not read resume: {exc}",
        ) from exc

    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No readable text was found in this resume.",
        )

    return {
        "filename": filename,
        "text": text,
    }

@router.post(
    "/api/resume/tailor",
    status_code=status.HTTP_200_OK,
    response_model=ResumeTailorResponse,
)
def resume_tailor(request: ResumeTailorRequest) -> ResumeTailorResponse:
    result = tailor_resume(
        request.resume_text,
        request.job_description,
    )

    try:
        response = ResumeTailorResponse(**result)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid resume tailoring result: {exc}",
        ) from exc

    return response