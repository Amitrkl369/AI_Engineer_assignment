from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from app.services.ocr import ocr_extract
from app.services.llm import parse_with_llm
from app.utils.confidence import combine_confidences

router = APIRouter()

@router.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    data = await file.read()
    max_bytes = 10 * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail="File too large (>10MB)")

    allowed = {"application/pdf", "image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    suffix = os.path.splitext(file.filename)[1] or (
        ".pdf" if file.content_type == "application/pdf" else ".jpg"
    )

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(data)
        tmp.flush()
        tmp.close()
        # OCR (raw text + token confidences)
        ocr_data = ocr_extract(tmp.name)
        raw_text = ocr_data.get("raw_text", "")
        # LLM parsing/structuring
        result = parse_with_llm(raw_text)
        # Combine OCR signals with LLM-provided confidences
        try:
            result = combine_confidences(result, ocr_data)
        except Exception:
            # if combining fails, continue returning LLM output
            pass
        return JSONResponse(content=result.dict())
    finally:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
