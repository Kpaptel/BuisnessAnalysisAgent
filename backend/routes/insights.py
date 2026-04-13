import os

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class InsightsRequest(BaseModel):
    metrics: dict = Field(..., description="Metrics object from /analyze or a row from /compare")
    context: str | None = Field(None, description="Optional extra context for the model")


def _placeholder_insights(metrics: dict, context: str | None) -> str:
    lines = [
        "AI insights are in placeholder mode. Set OPENAI_API_KEY to enable OpenAI explanations.",
        "",
        f"Summary from metrics: net profit {metrics.get('net_profit')}, "
        f"margin {metrics.get('profit_margin_percent')}%, "
        f"ROI {metrics.get('roi_percent')}% (if applicable).",
    ]
    if context:
        lines.append(f"Context noted: {context[:500]}")
    return "\n".join(lines)


@router.post("/insights")
async def generate_insights(body: InsightsRequest) -> dict:
    metrics = body.metrics
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "source": "placeholder",
            "text": _placeholder_insights(metrics, body.context),
        }

    prompt = (
        "You are a concise business analyst. Explain the deal in 3-5 bullet points for an investor. "
        "Use only the numbers provided; do not invent data.\n\n"
        f"Metrics JSON:\n{metrics}\n"
    )
    if body.context:
        prompt += f"\nExtra context:\n{body.context}\n"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    "messages": [
                        {"role": "system", "content": "You write clear, professional deal summaries."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.4,
                },
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {e!s}") from e

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {r.text}")

    data = r.json()
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=502, detail="Unexpected OpenAI response shape.") from e

    return {"source": "openai", "text": text}
