import io

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from utils.storage import file_store
from utils.validation import CSVValidationError, validate_financial_csv

router = APIRouter()


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")

    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {e!s}") from e

    try:
        validate_financial_csv(df)
    except CSVValidationError as e:
        raise HTTPException(status_code=422, detail=e.message) from e

    file_id = file_store.save(file.filename, df)
    return {
        "file_id": file_id,
        "filename": file.filename,
        "rows": int(len(df)),
        "columns": list(df.columns),
        "message": "File uploaded and validated.",
    }
