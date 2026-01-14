#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

SRTM_USGS = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/"
COPERNICUS_BUCKET_30M = "https://copernicus-dem-30m.s3.amazonaws.com/"
COPERNICUS_BUCKET_90M = "https://copernicus-dem-90m.s3.amazonaws.com/"
COPERNICUS_EULA_90M = "https://copernicus-dem-90m.s3.amazonaws.com/Copernicus_DSM_COG_30_N00_00_E006_00_DEM/INFO/eula_F.pdf"


def url_status(url: str) -> int:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status
    except Exception:
        return 0


def main() -> None:
    access_date = dt.datetime.now().strftime("%Y-%m-%d")
    srtm_status = url_status(SRTM_USGS)
    cop30_status = url_status(COPERNICUS_BUCKET_30M)
    cop90_status = url_status(COPERNICUS_BUCKET_90M)

    plan = "B" if cop90_status == 200 else "A"

    lines = [
        "# Topography features (elevation, slope, ruggedness)",
        "",
        f"- Accessed: {access_date}",
        f"- Plan chosen: {plan}",
        "",
        "## Plan A: SRTM 30m (NASA/USGS)",
        f"- URL (requires Earthdata auth): {SRTM_USGS}",
        f"- Status check: {srtm_status}",
        "",
        "## Plan B: Copernicus DEM GLO-90 (open S3 tiles)",
        f"- 30m bucket (too large for full tile download): {COPERNICUS_BUCKET_30M}",
        f"- 90m bucket used: {COPERNICUS_BUCKET_90M}",
        f"- Example EULA: {COPERNICUS_EULA_90M}",
        f"- Status check (90m bucket): {cop90_status}",
        "- Tile scheme: 1x1 degree COG tiles named `Copernicus_DSM_COG_30_[N/S]dd_00_[E/W]ddd_00_DEM`.",
        "- Resolution: 90m (3 arc-second).",
        "",
        "## Method",
        "- Use district capital points (ubigeo) to sample elevation, slope, and ruggedness.",
        "- Slope computed via finite differences on a 3x3 window; ruggedness as std dev of elevation in 3x3 window.",
        "",
        "## Limitations",
        "- Point-based sampling ignores intra-district heterogeneity.",
        "- Slope uses approximate meters-per-degree conversion; results are indicative.",
        "",
    ]

    out_path = DOCS_DIR / "TOPOGRAPHY_FEATURES.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
