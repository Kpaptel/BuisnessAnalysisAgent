from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from analysis import analyze_dataframe
from utils.storage import file_store

router = APIRouter()

#API requires a file id
class AnalyzeRequest(BaseModel):
    file_id: str = Field(..., description="ID returned from POST /upload")


@router.post("/analyze")
def analyze_file(body: AnalyzeRequest) -> dict:
    stored = file_store.get(body.file_id)
    #!test - is this raised when no file is uploaded?
    if not stored:
        raise HTTPException(status_code=404, detail="Unknown file_id. Upload the file first.")

    #customize deal name
    try:
        metrics = analyze_dataframe(stored.df, deal_label=stored.filename)
    #!customize exceptions
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    #!is this error proof? does one small error make the whole program crash?
    print("file_id: ", stored.file_id)

    return {
        "file_id": stored.file_id,
        "filename": stored.filename,
        "metrics": metrics,
    }
