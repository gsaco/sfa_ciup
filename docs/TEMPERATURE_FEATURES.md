# Temperature features (2023-2024)

- Accessed: 2026-01-13
- Decision: Plan A

## Plan A: TerraClimate (THREDDS)
- Official page: https://www.climatologylab.org/terraclimate.html
- THREDDS catalog (individual years): http://thredds.northwestknowledge.net:8080/thredds/catalog/TERRACLIMATE_ALL/data/catalog.html
- FileServer base: http://thredds.northwestknowledge.net:8080/thredds/fileServer/TERRACLIMATE_ALL/data
- Variables: tmax, tmin (monthly), compute tmean = (tmax + tmin)/2.
- Resolution: ~4km (1/24 degree).
- Coverage check: tmax/tmin 2023 and 2024 present in catalog = yes.
- Download method: NCSS subset by Peru bounding box to reduce size.

## Plan B (fallback): WorldClim monthly
- Official page: https://www.worldclim.org/data/monthlywthr.html
- Use only if TerraClimate annual files for 2023-2024 are unavailable.

## Limitations
- Gridded reanalysis-interpolated data; may smooth local extremes.
- Potential collinearity with region_natural and elevation; will check in robustness.
- 2024 data are recent and may be revised by source updates.
