"""Portable path configuration for this project.

Set SCDLP_DATA_ROOT to the analysis tree. If unset, paths use this project's
local data/ directory. Set SCDLP_ATLAS_PATH only to override the bundled atlas.
"""
from __future__ import annotations
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path(os.environ.get("SCDLP_DATA_ROOT", PROJECT_ROOT / "data")).expanduser().resolve()

def atlas_path() -> Path:
    configured = os.environ.get("SCDLP_ATLAS_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return PROJECT_ROOT / "test_data" / "atlas" / "Immune_All_Low.pkl"

def data_path(relative_path: str | os.PathLike[str]) -> Path:
    """Return a path under SCDLP_DATA_ROOT; reject absolute paths."""
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("data_path expects a relative path within SCDLP_DATA_ROOT")
    return DATA_ROOT / relative
