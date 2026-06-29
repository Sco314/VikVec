import json
from datetime import datetime, timezone
from pathlib import Path


def build_manifest(project_name: str = "VikVec", assets: list | None = None) -> dict:
    """Create a starter manifest dictionary."""
    return {
        "project_name": project_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "assets": assets or [],
    }


def write_manifest(manifest: dict, output_path: str | Path) -> Path:
    """Write a manifest to disk as JSON."""
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    return target


def load_manifest(manifest_path: str | Path) -> dict:
    """Read a manifest from disk."""
    path = Path(manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Manifest file was not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
