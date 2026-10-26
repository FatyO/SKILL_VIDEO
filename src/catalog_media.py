"""Catalog media files with FFprobe without modifying the originals."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


EXTENSIONS = {
    "video": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mts", ".m2ts"},
    "image": {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".opus", ".wma"},
}


def media_type(path: Path) -> str | None:
    suffix = path.suffix.lower()
    return next((kind for kind, values in EXTENSIONS.items() if suffix in values), None)


def number(value: Any) -> float | None:
    try:
        return round(float(value), 6)
    except (TypeError, ValueError):
        return None


def frame_rate(value: Any) -> float | None:
    if not value or value == "0/0":
        return None
    try:
        return round(float(Fraction(str(value))), 6)
    except (ValueError, ZeroDivisionError):
        return None


def run_ffprobe(path: Path, executable: str) -> tuple[dict[str, Any] | None, str | None]:
    command = [
        executable,
        "-v", "error",
        "-show_entries",
        "format=format_name,format_long_name,duration,size,bit_rate:"
        "stream=index,codec_type,codec_name,codec_long_name,width,height,"
        "r_frame_rate,avg_frame_rate,sample_rate,channels,channel_layout",
        "-of", "json",
        "--", str(path),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if result.returncode != 0:
        return None, (result.stderr.strip() or f"FFprobe termino con codigo {result.returncode}")
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"FFprobe devolvio JSON invalido: {exc}"


def inspect_file(path: Path, media_root: Path, ffprobe: str) -> dict[str, Any]:
    relative = path.relative_to(media_root).as_posix()
    kind = media_type(path)
    expected_folder = relative.split("/", 1)[0].lower()
    expected_kind = {"videos": "video", "images": "image", "audio": "audio"}.get(expected_folder)
    issues: list[dict[str, str]] = []

    if kind is None:
        issues.append({"severity": "error", "code": "unsupported_extension", "message": "Extension no admitida."})

    probe, error = run_ffprobe(path, ffprobe)
    if error:
        issues.append({"severity": "error", "code": "ffprobe_failed", "message": error})

    streams = (probe or {}).get("streams", [])
    video_streams = [item for item in streams if item.get("codec_type") == "video"]
    audio_streams = [item for item in streams if item.get("codec_type") == "audio"]

    if kind in {"video", "image"} and probe is not None and not video_streams:
        issues.append({"severity": "error", "code": "missing_video_stream", "message": "No se encontro una pista visual."})
    if kind == "audio" and probe is not None and not audio_streams:
        issues.append({"severity": "error", "code": "missing_audio_stream", "message": "No se encontro una pista de audio."})
    if kind and expected_kind and kind != expected_kind:
        issues.append({
            "severity": "warning",
            "code": "wrong_source_folder",
            "message": f"Es un archivo {kind}, pero esta dentro de media/{expected_folder}.",
        })

    visual = video_streams[0] if video_streams else {}
    audio = audio_streams[0] if audio_streams else {}
    format_info = (probe or {}).get("format", {})
    has_error = any(issue["severity"] == "error" for issue in issues)
    has_warning = any(issue["severity"] == "warning" for issue in issues)

    return {
        "id": hashlib.sha256(relative.encode("utf-8")).hexdigest()[:16],
        "path": relative,
        "absolute_path": str(path.resolve()),
        "file_name": path.name,
        "extension": path.suffix.lower(),
        "media_type": kind or "unknown",
        "size_bytes": path.stat().st_size,
        "status": "incompatible" if has_error else ("warning" if has_warning else "compatible"),
        "issues": issues,
        "metadata": {
            "format": format_info.get("format_name"),
            "format_long_name": format_info.get("format_long_name"),
            "duration_seconds": number(format_info.get("duration")) if kind in {"video", "audio"} else None,
            "bit_rate": int(format_info["bit_rate"]) if str(format_info.get("bit_rate", "")).isdigit() else None,
            "width": visual.get("width"),
            "height": visual.get("height"),
            "fps": frame_rate(visual.get("avg_frame_rate") or visual.get("r_frame_rate")) if kind == "video" else None,
            "video_codec": visual.get("codec_name"),
            "audio_codec": audio.get("codec_name"),
            "sample_rate_hz": int(audio["sample_rate"]) if str(audio.get("sample_rate", "")).isdigit() else None,
            "audio_channels": audio.get("channels"),
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def build_catalog(media_root: Path, catalog_root: Path, batch_size: int, ffprobe: str) -> dict[str, Any]:
    files = sorted((path for path in media_root.rglob("*") if path.is_file()), key=lambda item: item.as_posix().lower())
    records = [inspect_file(path, media_root, ffprobe) for path in files]
    usable_videos = [item for item in records if item["media_type"] == "video" and item["status"] != "incompatible"]

    batches = []
    for offset in range(0, len(usable_videos), batch_size):
        items = usable_videos[offset:offset + batch_size]
        batch_name = f"batch_{offset // batch_size + 1:03d}"
        manifest = {
            "batch": batch_name,
            "batch_size": batch_size,
            "video_count": len(items),
            "complete": len(items) == batch_size,
            "videos": [{"id": item["id"], "path": item["path"], "absolute_path": item["absolute_path"]} for item in items],
        }
        manifest_path = catalog_root / "batches" / batch_name / "manifest.json"
        write_json(manifest_path, manifest)
        batches.append({"name": batch_name, "manifest": manifest_path.relative_to(catalog_root).as_posix(), **manifest})

    counts = {kind: sum(item["media_type"] == kind for item in records) for kind in ("video", "image", "audio", "unknown")}
    counts.update({
        "compatible": sum(item["status"] == "compatible" for item in records),
        "warnings": sum(item["status"] == "warning" for item in records),
        "incompatible": sum(item["status"] == "incompatible" for item in records),
    })
    catalog = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "media_root": str(media_root.resolve()),
        "originals_modified": False,
        "batch_size": batch_size,
        "summary": counts,
        "batches": batches,
        "files": records,
    }
    write_json(catalog_root / "media_catalog.json", catalog)
    return catalog


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Cataloga multimedia con FFprobe y agrupa videos sin mover originales.")
    parser.add_argument("--media-root", type=Path, default=project_root / "media")
    parser.add_argument("--catalog-root", type=Path, default=project_root / "output" / "catalog")
    parser.add_argument("--batch-size", type=int, default=3)
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size debe ser mayor que cero")
    return args


def main() -> int:
    args = parse_args()
    if not args.media_root.is_dir():
        print(f"No existe la carpeta de medios: {args.media_root}", file=sys.stderr)
        return 2
    if shutil.which(args.ffprobe) is None:
        print(f"No se encontro FFprobe: {args.ffprobe}", file=sys.stderr)
        return 2
    catalog = build_catalog(args.media_root.resolve(), args.catalog_root.resolve(), args.batch_size, args.ffprobe)
    summary = catalog["summary"]
    print(f"Archivos analizados: {len(catalog['files'])}")
    print(f"Videos: {summary['video']} | Imagenes: {summary['image']} | Audio: {summary['audio']}")
    print(f"Compatibles: {summary['compatible']} | Avisos: {summary['warnings']} | Incompatibles: {summary['incompatible']}")
    print(f"Lotes de video: {len(catalog['batches'])}")
    print(f"Catalogo: {args.catalog_root.resolve() / 'media_catalog.json'}")
    return 1 if summary["incompatible"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

