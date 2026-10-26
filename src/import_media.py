"""Importa archivos multimedia al proyecto sin modificar los originales."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


EXTENSIONS = {
    "images": {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"},
    "videos": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mts", ".m2ts"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".opus", ".wma"},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def destination_folder(path: Path, media_root: Path, collection: str | None) -> Path | None:
    suffix = path.suffix.lower()
    for folder, extensions in EXTENSIONS.items():
        if suffix in extensions:
            if folder == "images" and collection:
                return media_root / folder / "collections" / collection
            return media_root / folder
    return None


def unique_destination(source: Path, folder: Path) -> tuple[Path, bool]:
    source_hash = sha256(source)
    candidate = folder / source.name
    if candidate.exists() and sha256(candidate) == source_hash:
        return candidate, True

    counter = 2
    while candidate.exists():
        candidate = folder / f"{source.stem}-{counter}{source.suffix.lower()}"
        if sha256(candidate) == source_hash:
            return candidate, True
        counter += 1
    return candidate, False


def import_file(source: Path, media_root: Path, collection: str | None) -> tuple[str, Path | None]:
    if not source.is_file():
        return "no_encontrado", None
    folder = destination_folder(source, media_root, collection)
    if folder is None:
        return "no_compatible", None
    folder.mkdir(parents=True, exist_ok=True)
    destination, duplicate = unique_destination(source, folder)
    if duplicate:
        return "ya_existia", destination
    shutil.copy2(source, destination)
    return "copiado", destination


def next_collection(media_root: Path) -> str:
    collections_root = media_root / "images" / "collections"
    existing = {
        path.name
        for path in collections_root.glob("video_[0-9][0-9][0-9]")
        if path.is_dir()
    } if collections_root.exists() else set()
    index = 1
    while f"video_{index:03d}" in existing:
        index += 1
    return f"video_{index:03d}"


def save_active_collection(project_root: Path, collection: str) -> None:
    state_path = project_root / "output" / "catalog" / "active_image_collection.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps({
            "collection": collection,
            "path": f"media/images/collections/{collection}",
            "selection_rule": "use_only_this_collection",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Copia imágenes, videos y audios a media/ sin alterar los originales."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Archivos externos que se importarán.")
    parser.add_argument("--media-root", type=Path, default=project_root / "media")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--collection", help="Colección de imágenes existente, por ejemplo video_002.")
    group.add_argument("--new-collection", action="store_true", help="Crea una colección video_NNN nueva.")
    args = parser.parse_args()

    media_root = args.media_root.resolve()
    collection = next_collection(media_root) if args.new_collection else args.collection
    if collection:
        save_active_collection(project_root, collection)
        print(f"coleccion_activa: {collection}")

    exit_code = 0
    for raw_path in args.paths:
        source = raw_path.expanduser().resolve()
        status, destination = import_file(source, media_root, collection)
        if status in {"no_encontrado", "no_compatible"}:
            exit_code = 1
        target = str(destination) if destination else "-"
        print(f"{status}: {source} -> {target}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
