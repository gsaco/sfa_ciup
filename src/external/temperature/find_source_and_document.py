#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

TERRACLIMATE_PAGE = "https://www.climatologylab.org/terraclimate.html"
TERRACLIMATE_CATALOG = "http://thredds.northwestknowledge.net:8080/thredds/catalog/TERRACLIMATE_ALL/data/catalog.html"
TERRACLIMATE_FILESERVER = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/TERRACLIMATE_ALL/data"
WORLDCLIM_PAGE = "https://www.worldclim.org/data/monthlywthr.html"


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def main() -> None:
    access_date = dt.datetime.now().strftime("%Y-%m-%d")
    page_text = fetch_text(TERRACLIMATE_PAGE)
    catalog_text = fetch_text(TERRACLIMATE_CATALOG)

    has_2023 = "TerraClimate_tmax_2023.nc" in catalog_text and "TerraClimate_tmin_2023.nc" in catalog_text
    has_2024 = "TerraClimate_tmax_2024.nc" in catalog_text and "TerraClimate_tmin_2024.nc" in catalog_text

    plan = "A" if (has_2023 and has_2024) else "B"

    lines = [
        "# Temperature features (2023-2024)",
        "",
        f"- Accessed: {access_date}",
        "- Decision: Plan {}".format(plan),
        "",
        "## Plan A: TerraClimate (THREDDS)",
        "- Official page: {}".format(TERRACLIMATE_PAGE),
        "- THREDDS catalog (individual years): {}".format(TERRACLIMATE_CATALOG),
        "- FileServer base: {}".format(TERRACLIMATE_FILESERVER),
        "- Variables: tmax, tmin (monthly), compute tmean = (tmax + tmin)/2.",
        "- Resolution: ~4km (1/24 degree).",
        "- Coverage check: tmax/tmin 2023 and 2024 present in catalog = {}.".format("yes" if (has_2023 and has_2024) else "no"),
        "- Download method: NCSS subset by Peru bounding box to reduce size.",
        "",
        "## Plan B (fallback): WorldClim monthly",
        "- Official page: {}".format(WORLDCLIM_PAGE),
        "- Use only if TerraClimate annual files for 2023-2024 are unavailable.",
        "",
        "## Limitations",
        "- Gridded reanalysis-interpolated data; may smooth local extremes.",
        "- Potential collinearity with region_natural and elevation; will check in robustness.",
        "- 2024 data are recent and may be revised by source updates.",
        "",
    ]

    out_path = DOCS_DIR / "TEMPERATURE_FEATURES.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
