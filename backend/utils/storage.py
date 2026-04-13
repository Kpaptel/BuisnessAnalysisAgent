import uuid
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class StoredFile:
    file_id: str
    filename: str
    df: pd.DataFrame


class FileStore:
    def __init__(self) -> None:
        self._items: dict[str, StoredFile] = {}

    def save(self, filename: str, df: pd.DataFrame) -> str:
        file_id = str(uuid.uuid4())
        self._items[file_id] = StoredFile(file_id=file_id, filename=filename, df=df)
        return file_id

    def get(self, file_id: str) -> StoredFile | None:
        return self._items.get(file_id)

    def get_many(self, file_ids: list[str]) -> list[StoredFile]:
        return [self._items[fid] for fid in file_ids if fid in self._items]

    def delete(self, file_id: str) -> bool:
        return self._items.pop(file_id, None) is not None

    def list_ids(self) -> list[str]:
        return list(self._items.keys())


file_store = FileStore()
