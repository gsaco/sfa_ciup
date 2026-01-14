# Topography features (elevation, slope, ruggedness)

- Accessed: 2026-01-13
- Plan chosen: B

## Plan A: SRTM 30m (NASA/USGS)
- URL (requires Earthdata auth): https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/
- Status check: 0

## Plan B: Copernicus DEM GLO-90 (open S3 tiles)
- 30m bucket (too large for full tile download): https://copernicus-dem-30m.s3.amazonaws.com/
- 90m bucket used: https://copernicus-dem-90m.s3.amazonaws.com/
- Example EULA: https://copernicus-dem-90m.s3.amazonaws.com/Copernicus_DSM_COG_30_N00_00_E006_00_DEM/INFO/eula_F.pdf
- Status check (90m bucket): 200
- Tile scheme: 1x1 degree COG tiles named `Copernicus_DSM_COG_30_[N/S]dd_00_[E/W]ddd_00_DEM`.
- Resolution: 90m (3 arc-second).

## Method
- Use district capital points (ubigeo) to sample elevation, slope, and ruggedness.
- Slope computed via finite differences on a 3x3 window; ruggedness as std dev of elevation in 3x3 window.

## Limitations
- Point-based sampling ignores intra-district heterogeneity.
- Slope uses approximate meters-per-degree conversion; results are indicative.
