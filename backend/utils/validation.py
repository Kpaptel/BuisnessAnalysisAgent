import pandas as pd

from analysis import REQUIRED_NUMERIC_KINDS, resolve_metric_columns


class CSVValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def validate_financial_csv(df: pd.DataFrame) -> None:
    if df is None or df.empty:
        raise CSVValidationError("CSV is empty or could not be parsed.")

    resolved = resolve_metric_columns(df)
    missing = [name for name, col in resolved.items() if col is None and name in REQUIRED_NUMERIC_KINDS]
    if missing:
        raise CSVValidationError(
            f"Missing required financial columns. Need at least one of the synonyms for: {', '.join(missing)}. "
            f"Found columns: {list(df.columns)}"
        )
