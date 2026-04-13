from __future__ import annotations

from typing import Any

import pandas as pd

REVENUE_SYNONYMS = ("revenue", "sales", "total_revenue", "income", "gross_revenue")
EXPENSE_SYNONYMS = ("expenses", "expense", "costs", "cost", "cogs", "operating_expenses")
ASKING_PRICE_SYNONYMS = ("asking_price", "purchase_price", "acquisition_cost", "price", "deal_price")


def _normalize_name(name: str) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def _column_map(df: pd.DataFrame) -> dict[str, str]:
    return {_normalize_name(c): c for c in df.columns}


def _pick_column(norm_map: dict[str, str], synonyms: tuple[str, ...]) -> str | None:
    for syn in synonyms:
        if syn in norm_map:
            return norm_map[syn]
    return None


def resolve_metric_columns(df: pd.DataFrame) -> dict[str, str | None]:
    nm = _column_map(df)
    return {
        "revenue": _pick_column(nm, REVENUE_SYNONYMS),
        "expenses": _pick_column(nm, EXPENSE_SYNONYMS),
        "asking_price": _pick_column(nm, ASKING_PRICE_SYNONYMS),
    }


REQUIRED_NUMERIC_KINDS = ("revenue", "expenses")


def _to_numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    s = pd.to_numeric(df[col], errors="coerce")
    return s.fillna(0)


def analyze_dataframe(df: pd.DataFrame, deal_label: str | None = None) -> dict[str, Any]:
    resolved = resolve_metric_columns(df)
    rev_col = resolved["revenue"]
    exp_col = resolved["expenses"]
    price_col = resolved["asking_price"]

    if rev_col is None or exp_col is None:
        raise ValueError("DataFrame must include resolvable revenue and expenses columns.")

    revenue = float(_to_numeric_series(df, rev_col).sum())
    expenses = float(_to_numeric_series(df, exp_col).sum())
    net_profit = revenue - expenses
    profit_margin = float((net_profit / revenue) * 100) if revenue != 0 else 0.0

    asking_used: float | None = None
    roi: float | None = None
    if price_col is not None:
        prices = _to_numeric_series(df, price_col)
        nonzero = prices[prices != 0]
        if not nonzero.empty:
            asking_used = float(nonzero.iloc[0])
        elif not prices.empty:
            asking_used = float(prices.iloc[0])
        if asking_used is not None and asking_used != 0:
            roi = float((net_profit / asking_used) * 100)

    return {
        "deal_label": deal_label,
        "total_revenue": round(revenue, 2),
        "total_expenses": round(expenses, 2),
        "net_profit": round(net_profit, 2),
        "profit_margin_percent": round(profit_margin, 2),
        "roi_percent": None if roi is None else round(roi, 2),
        "asking_price_used": None if asking_used is None else round(asking_used, 2),
    }


def compare_deals(metrics_list: list[dict[str, Any]]) -> dict[str, Any]:
    if not metrics_list:
        return {
            "deals": [],
            "rankings": {"by_roi": [], "by_profit": [], "by_margin": []},
            "best_deal": None,
        }

    enriched: list[dict[str, Any]] = []
    for i, m in enumerate(metrics_list):
        row = {**m, "_index": i}
        enriched.append(row)

    def sort_key_roi(x: dict[str, Any]) -> float:
        v = x.get("roi_percent")
        return float("-inf") if v is None else float(v)

    def sort_key_profit(x: dict[str, Any]) -> float:
        return float(x.get("net_profit") or 0)

    def sort_key_margin(x: dict[str, Any]) -> float:
        return float(x.get("profit_margin_percent") or 0)

    by_roi = sorted(enriched, key=sort_key_roi, reverse=True)
    by_profit = sorted(enriched, key=sort_key_profit, reverse=True)
    by_margin = sorted(enriched, key=sort_key_margin, reverse=True)

    best = by_profit[0]
    best_reason = "Highest net profit among compared deals."
    if all(m.get("roi_percent") is not None for m in enriched):
        best_roi = by_roi[0]
        if best_roi["_index"] != best["_index"]:
            best = best_roi
            best_reason = "Highest ROI among compared deals (all deals had asking price)."

    best_deal = {k: v for k, v in best.items() if not k.startswith("_")}
    best_deal["recommendation_reason"] = best_reason

    return {
        "deals": metrics_list,
        "rankings": {
            "by_roi": [_strip_internal(d) for d in by_roi],
            "by_profit": [_strip_internal(d) for d in by_profit],
            "by_margin": [_strip_internal(d) for d in by_margin],
        },
        "best_deal": best_deal,
    }


def _strip_internal(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if not k.startswith("_")}
