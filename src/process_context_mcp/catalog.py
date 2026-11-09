"""Loading and querying the process catalog."""

from __future__ import annotations

import json
import os
from importlib import resources
from pathlib import Path

from pydantic import BaseModel, TypeAdapter

CATALOG_ENV_VAR = "PROCESS_CATALOG_PATH"


class Step(BaseModel):
    order: int
    name: str
    role: str


class Process(BaseModel):
    id: str
    name: str
    description: str
    owner: str
    steps: list[Step]


class ProcessSummary(BaseModel):
    id: str
    name: str
    owner: str


class ProcessCatalog:
    def __init__(self, processes: list[Process]) -> None:
        self._processes = {process.id: process for process in processes}

    @classmethod
    def from_file(cls, path: Path) -> ProcessCatalog:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls(TypeAdapter(list[Process]).validate_python(raw))

    @classmethod
    def load(cls) -> ProcessCatalog:
        """Load the catalog from PROCESS_CATALOG_PATH, or the bundled catalog if unset."""
        custom_path = os.environ.get(CATALOG_ENV_VAR)
        if custom_path:
            return cls.from_file(Path(custom_path))
        bundled = resources.files("process_context_mcp") / "data" / "processes.json"
        with resources.as_file(bundled) as path:
            return cls.from_file(path)

    @property
    def ids(self) -> list[str]:
        return sorted(self._processes)

    def summaries(self) -> list[ProcessSummary]:
        return [
            ProcessSummary(id=p.id, name=p.name, owner=p.owner)
            for p in sorted(self._processes.values(), key=lambda p: p.id)
        ]

    def get(self, process_id: str) -> Process | None:
        return self._processes.get(process_id)
