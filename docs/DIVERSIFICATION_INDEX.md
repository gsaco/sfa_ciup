# Diversification Index

## Main measure
- **Basis**: harvested area per crop (`P217_SUP_ha` from `03_CAP200AB.csv`).
- **Share**: \( s_{i} = \frac{\text{area}_{i}}{\sum_{j}\text{area}_{j}} \) at producer level.
- **HHI**: \( \text{HHI} = \sum_i s_i^2 \).
- **Diversification**: \( 1 - \text{HHI} \).

## Alternatives (robustness)
- Shannon entropy: \( -\sum_i s_i \log(s_i) \).
- Number of crops (distinct `P204_COD`).

## QA checks
- Shares sum to ~1 for producers with positive total area.
- HHI in [0, 1].
- Single-crop producers: HHI = 1 and diversification = 0.

## Notes
- Producers with zero/negative total harvested area are left as missing for share-based indices.
