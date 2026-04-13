from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from analysis import analyze_dataframe, compare_deals
from utils.storage import file_store

router = APIRouter()


class CompareRequest(BaseModel):
    file_ids: list[str] = Field(..., min_length=1, description="IDs from POST /upload")


@router.post("/compare")
def compare_files(body: CompareRequest) -> dict:
    stored_list = file_store.get_many(body.file_ids)
    if len(stored_list) != len(body.file_ids):
        missing = set(body.file_ids) - {s.file_id for s in stored_list}
        raise HTTPException(status_code=404, detail=f"Unknown file_id(s): {sorted(missing)}")

    metrics_list: list[dict] = []
    for s in stored_list:
        try:
            m = analyze_dataframe(s.df, deal_label=s.filename)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"{s.filename}: {e}") from e
        m["file_id"] = s.file_id
        m["filename"] = s.filename
        metrics_list.append(m)

    comparison = compare_deals(metrics_list)
    return comparison
