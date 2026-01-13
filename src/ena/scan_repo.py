#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import os
import re
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
DOCS_DIR = REPO_ROOT / "docs"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"


def human_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024**2:
        return f"{num_bytes / 1024:.2f} KB"
    if num_bytes < 1024**3:
        return f"{num_bytes / 1024**2:.2f} MB"
    return f"{num_bytes / 1024**3:.2f} GB"


def build_tree(root: Path, max_depth: int = 3) -> list[str]:
    lines: list[str] = []
    for current_root, dirs, files in os.walk(root):
        rel = Path(current_root).relative_to(root)
        depth = len(rel.parts)
        if depth > max_depth:
            dirs[:] = []
            continue
        if any(part.startswith(".") for part in rel.parts):
            continue
        dirs[:] = sorted(dirs)
        files = sorted(files)
        indent = "  " * depth
        folder_label = "." if depth == 0 else rel.name
        lines.append(f"{indent}{folder_label}/")
        if depth < max_depth:
            for fname in files:
                if fname.startswith("."):
                    continue
                lines.append(f"{indent}  {fname}")
    return lines


def infer_year(path_str: str) -> str:
    match = re.findall(r"(20\d{2})", path_str)
    if match:
        return match[-1]
    return ""


def infer_module(path_str: str) -> str:
    match = re.search(r"Modulo(\d+)", path_str, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def list_data_files(data_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for current_root, dirs, files in os.walk(data_dir):
        rel = Path(current_root).relative_to(data_dir)
        if rel.parts and rel.parts[0] in {"intermediate", "processed"}:
            dirs[:] = []
            continue
        dirs[:] = sorted(dirs)
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            paths.append(Path(current_root) / fname)
    return paths


def summarize_extensions(paths: list[Path]) -> list[tuple[str, int, int]]:
    buckets: dict[str, list[int]] = defaultdict(list)
    for path in paths:
        ext = path.suffix.lower() if path.suffix else "(no_ext)"
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        buckets[ext].append(size)
    summary = []
    for ext, sizes in sorted(buckets.items(), key=lambda item: item[0]):
        summary.append((ext, len(sizes), sum(sizes)))
    return summary


def write_manifest(paths: list[Path], output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["nombre_archivo", "ruta", "tipo", "anio", "modulo"],
        )
        writer.writeheader()
        for path in sorted(paths):
            rel = path.relative_to(REPO_ROOT)
            writer.writerow(
                {
                    "nombre_archivo": path.name,
                    "ruta": rel.as_posix(),
                    "tipo": path.suffix.lower().lstrip("."),
                    "anio": infer_year(rel.as_posix()),
                    "modulo": infer_module(rel.as_posix()),
                }
            )


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

    tree_lines = build_tree(REPO_ROOT, max_depth=3)

    data_files = list_data_files(DATA_DIR)
    extension_summary = summarize_extensions(data_files)

    ena_root = DATA_DIR / "raw" / "ENA_2024"
    ena_zip = DATA_DIR / "ENA_2024.zip"
    dict_path = REPO_ROOT / "DICCIONARIO DE DATOS ENA-2024.pdf"

    def safe_size(path: Path) -> str:
        try:
            return human_size(path.stat().st_size)
        except OSError:
            return "NA"

    inventory_path = DOCS_DIR / "REPO_INVENTORY.md"
    with inventory_path.open("w", encoding="utf-8") as handle:
        handle.write("# Repo Inventory\n\n")
        handle.write(f"- Generated: {dt.datetime.now().isoformat(timespec='seconds')}\n")
        handle.write(f"- Repo root: `{REPO_ROOT}`\n\n")

        handle.write("## Tree (depth <= 3)\n\n")
        handle.write("```\n")
        handle.write("\n".join(tree_lines))
        handle.write("\n```\n\n")

        handle.write("## ENA 2024 data locations\n\n")
        handle.write(f"- Raw ENA 2024 folder: `{ena_root}` (exists: {ena_root.exists()})\n")
        handle.write(f"- Raw ENA 2024 zip: `{ena_zip}` (exists: {ena_zip.exists()}, size: {safe_size(ena_zip)})\n")
        handle.write(f"- Data README: `{DATA_DIR / 'README.md'}` (exists: {(DATA_DIR / 'README.md').exists()})\n\n")

        handle.write("## Variable dictionary\n\n")
        handle.write(f"- Dictionary file: `{dict_path}` (exists: {dict_path.exists()}, size: {safe_size(dict_path)})\n\n")

        handle.write("## Existing scripts that read ENA\n\n")
        handle.write("- None found in repo at scan time.\n\n")

        handle.write("## Data formats and approximate sizes\n\n")
        handle.write("| Extension | Count | Total size |\n")
        handle.write("|---|---:|---:|\n")
        for ext, count, total in extension_summary:
            handle.write(f"| {ext} | {count} | {human_size(total)} |\n")
        handle.write("\n")

    manifest_path = INTERMEDIATE_DIR / "raw_manifest.csv"
    write_manifest(data_files, manifest_path)

    print(f"Wrote {inventory_path}")
    print(f"Wrote {manifest_path}")
    print(f"Data files scanned: {len(data_files)}")


if __name__ == "__main__":
    main()
