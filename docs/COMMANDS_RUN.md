timestamp | command | exit_code
2026-01-13T20:11:52-05:00 | init docs/COMMANDS_RUN.md header | exit 0
2026-01-13T20:11:54-05:00 | ls | exit 0
2026-01-13T20:11:59-05:00 | command -v tree | exit 1
2026-01-13T20:12:06-05:00 | find . -maxdepth 4 -path './.git' -prune -o -print | sed 's|^\./||' > docs/REPO_TREE.txt | exit 0
2026-01-13T20:12:11-05:00 | rg --files -g 'Makefile' -g 'makefile' -g 'run_all*' -g '*.sh' | exit 0
2026-01-13T20:12:16-05:00 | sed -n '1,200p' scripts/run_all.sh | exit 0
2026-01-13T20:12:21-05:00 | sed -n '1,200p' src/report/build_report.py | exit 0
2026-01-13T20:12:25-05:00 | sed -n '200,400p' src/report/build_report.py | exit 0
2026-01-13T20:12:28-05:00 | sed -n '400,800p' src/report/build_report.py | exit 0
2026-01-13T20:20:56-05:00 | bash scripts/run_all.sh | tee logs/run_all_baseline.log | exit 0
2026-01-13T20:21:14-05:00 | sed -n '1,240p' src/ena/05_build_model_data.py | exit 0
2026-01-13T20:21:22-05:00 | rg -n "P301A" docs/ENA2024_VARIABLE_DICTIONARY.md | exit 0
2026-01-13T20:21:29-05:00 | command -v pdftotext | exit 0
2026-01-13T20:21:39-05:00 | pdftotext 'DICCIONARIO DE DATOS ENA-2024.pdf' - | rg -n 'P301A_' | exit 0
2026-01-13T20:21:46-05:00 | pdftotext 'DICCIONARIO DE DATOS ENA-2024.pdf' /tmp/ena_dict.txt | exit 0
2026-01-13T20:21:51-05:00 | sed -n '7035,7075p' /tmp/ena_dict.txt | exit 0
2026-01-13T20:22:10-05:00 | python - <<'PY' (inspect P301A values) | exit 0
2026-01-13T20:22:27-05:00 | python - <<'PY' (model_data_ena2024 key summaries) | exit 1
2026-01-13T20:22:40-05:00 | ./venv/bin/python - <<'PY' (model_data_ena2024 key summaries) | exit 0
2026-01-13T20:22:46-05:00 | rg -n "NSEGM" docs/ENA2024_VARIABLE_DICTIONARY.md | exit 0
2026-01-13T20:22:52-05:00 | rg -n "FACTOR_PRODUCTOR|ESTRATO" docs/ENA2024_VARIABLE_DICTIONARY.md | exit 0
2026-01-13T20:22:58-05:00 | sed -n '1,240p' src/ena/04_compute_diversification.py | exit 0
2026-01-13T20:23:04-05:00 | sed -n '1,240p' src/ena/02_build_schema_from_dictionary.py | exit 0
2026-01-13T20:23:09-05:00 | sed -n '1,240p' src/ena/06_build_model_data_plus_controls.py | exit 0
2026-01-13T20:23:14-05:00 | sed -n '1,260p' src/features/ena_controls.py | exit 0
2026-01-13T20:23:24-05:00 | sed -n '1,240p' R/01_sfa_main.R | exit 0
2026-01-13T20:23:28-05:00 | sed -n '240,480p' R/01_sfa_main.R | exit 0
2026-01-13T20:23:33-05:00 | sed -n '480,960p' R/01_sfa_main.R | exit 0
2026-01-13T20:23:39-05:00 | sed -n '1,240p' R/02_logit_practices.R | exit 0
2026-01-13T20:23:44-05:00 | sed -n '240,480p' R/02_logit_practices.R | exit 0
2026-01-13T20:23:57-05:00 | ./venv/bin/python - <<'PY' (psu/strata audit) | exit 0
2026-01-13T20:24:06-05:00 | rg -n "P220_1_VAL" /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:11-05:00 | sed -n '4038,4058p' /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:16-05:00 | rg -n "P237_VAL|P239|P241" /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:21-05:00 | sed -n '6685,6705p' /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:27-05:00 | sed -n '6790,6822p' /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:35-05:00 | rg -n "P212|P213" /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:40-05:00 | sed -n '3905,3935p' /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:46-05:00 | rg -n "P212" /tmp/ena_dict.txt | exit 0
2026-01-13T20:24:52-05:00 | sed -n '3910,3955p' /tmp/ena_dict.txt | exit 0
2026-01-13T20:25:02-05:00 | ./venv/bin/python - <<'PY' (water_source/irrigation_system distribution) | exit 0
2026-01-13T20:25:19-05:00 | ./venv/bin/python - <<'PY' (controls distribution) | exit 0
2026-01-13T20:25:28-05:00 | ./venv/bin/python - <<'PY' (diversification checks) | exit 0
2026-01-13T20:25:38-05:00 | ./venv/bin/python - <<'PY' (practice_any crosstabs) | exit 0
2026-01-13T20:25:45-05:00 | ./venv/bin/python - <<'PY' (print 02_sfa_main.csv) | exit 0
2026-01-13T20:25:53-05:00 | ./venv/bin/python - <<'PY' (sfa main estimates) | exit 0
2026-01-13T20:26:06-05:00 | ./venv/bin/python - <<'PY' (TE summaries) | exit 1
2026-01-13T20:26:17-05:00 | ./venv/bin/python - <<'PY' (TE merge with type fix) | exit 0
2026-01-13T20:26:30-05:00 | ./venv/bin/python - <<'PY' (TE key samples) | exit 0
2026-01-13T20:26:41-05:00 | ./venv/bin/python - <<'PY' (TE merge normalized keys) | exit 0
2026-01-13T20:26:51-05:00 | ./venv/bin/python - <<'PY' (print 04_logit_main.csv) | exit 0
2026-01-13T20:26:58-05:00 | ./venv/bin/python - <<'PY' (print 05_logit_robustness.csv) | exit 0
2026-01-13T20:27:05-05:00 | ./venv/bin/python - <<'PY' (logit robustness details) | exit 0
2026-01-13T20:27:12-05:00 | sed -n '1,260p' src/features/merge_geo_features.py | exit 0
2026-01-13T20:27:16-05:00 | sed -n '1,260p' src/features/merge_temperature_features.py | exit 0
2026-01-13T20:27:22-05:00 | sed -n '1,260p' src/features/merge_geo2_features.py | exit 0
2026-01-13T20:27:39-05:00 | ./venv/bin/python - <<'PY' (geo coverage) | exit 0
2026-01-13T20:27:44-05:00 | ./venv/bin/python - <<'PY' (temp_topo coverage) | exit 0
2026-01-13T20:27:59-05:00 | ./venv/bin/python - <<'PY' (geo/climate ranges) | exit 0
2026-01-13T20:28:08-05:00 | ./venv/bin/python - <<'PY' (geo2 correlation) | exit 0
2026-01-13T20:28:24-05:00 | rg -n "CONG|CONGLO|UPM|UPA|SEGMENTO|NSEGM" docs/ENA2024_VARIABLE_DICTIONARY.md | exit 0
2026-01-13T20:28:38-05:00 | ./venv/bin/python - <<'PY' (sample sizes) | exit 0
2026-01-13T20:28:49-05:00 | rg -n "Warning|warning|ERROR|Error|RuntimeWarning" logs/run_all_baseline.log | exit 0
2026-01-13T20:28:55-05:00 | sed -n '60,130p' logs/run_all_baseline.log | exit 0
2026-01-13T20:29:08-05:00 | ./venv/bin/python - <<'PY' (area_total_ha missing by region) | exit 0
2026-01-13T20:29:15-05:00 | ./venv/bin/python - <<'PY' (valor_total missing by region) | exit 0
2026-01-13T20:29:25-05:00 | ./venv/bin/python - <<'PY' (check geopandas) | exit 1
2026-01-13T20:29:32-05:00 | rg --files -g '*.shp' -g '*.geojson' -g '*.gpkg' | exit 1
2026-01-13T20:29:39-05:00 | rg -n "plots" src R docs | exit 0
2026-01-13T20:29:50-05:00 | ./venv/bin/python - <<'PY' (check matplotlib/seaborn) | exit 1
2026-01-13T20:29:55-05:00 | cat requirements.txt | exit 0
2026-01-13T20:30:08-05:00 | ./venv/bin/pip install matplotlib seaborn | exit 0
2026-01-13T20:31:41-05:00 | ./venv/bin/python - <<'PY' (TE vs diversification bins) | exit 0
2026-01-13T20:31:50-05:00 | ./venv/bin/python - <<'PY' (sample_loss_analysis) | exit 0
2026-01-13T20:32:12-05:00 | ls docs | exit 0
2026-01-13T20:32:19-05:00 | sed -n '1,200p' docs/CHANGELOG.md | exit 0
2026-01-13T20:32:26-05:00 | cat outputs/manifest.json | exit 0
2026-01-13T20:32:34-05:00 | ./venv/bin/python - <<'PY' (P810 values) | exit 0
2026-01-13T20:32:43-05:00 | ./venv/bin/python - <<'PY' (P236/P238 values) | exit 0
2026-01-13T20:32:50-05:00 | ./venv/bin/python - <<'PY' (P1206 values) | exit 0
2026-01-13T20:32:58-05:00 | ./venv/bin/python - <<'PY' (P701/P704 values) | exit 0
2026-01-13T20:33:06-05:00 | ./venv/bin/python - <<'PY' (P902 values) | exit 0
2026-01-13T20:33:13-05:00 | ./venv/bin/python - <<'PY' (P801 values) | exit 0
2026-01-13T20:33:20-05:00 | sed -n '1,240p' reports/reporte_final.md | exit 0
2026-01-13T20:35:48-05:00 | ./venv/bin/python scripts/plot_pack.py | exit 0
2026-01-13T20:35:53-05:00 | rg --files outputs/plots | exit 0
2026-01-13T20:36:16-05:00 | ./venv/bin/python - <<'PY' (plot validation stats) | exit 0
2026-01-13T20:37:01-05:00 | cat <<'EOF' > outputs/plots/00_index/plot_manifest.md | exit 0
2026-01-13T20:37:27-05:00 | cat <<'EOF' > docs/ERROR_LEDGER.md | exit 0
2026-01-13T20:37:48-05:00 | cat <<'EOF' > docs/VARIABLE_DEFINITIONS_AUDIT.md | exit 0
2026-01-13T20:38:00-05:00 | ./venv/bin/python - <<'PY' (estrato/psu missing logit) | exit 0
2026-01-13T20:38:13-05:00 | cat <<'EOF' > docs/SURVEY_DESIGN_AUDIT.md | exit 0
2026-01-13T20:38:29-05:00 | cat <<'EOF' > docs/SFA_INTERPRETATION_AUDIT.md | exit 0
2026-01-13T20:38:45-05:00 | cat <<'EOF' > docs/GEO_CLIMATE_AUDIT.md | exit 0
2026-01-13T20:38:59-05:00 | cat <<'EOF' > docs/INTUITION_VS_RESULTS.md | exit 0
2026-01-13T20:39:22-05:00 | cat <<'EOF' > docs/DEEP_AUDIT_REPORT.md | exit 0
2026-01-13T20:39:35-05:00 | cat <<'EOF' >> docs/CHANGELOG.md | exit 0
2026-01-13T20:40:27-05:00 | ./venv/bin/python src/report/build_report.py | exit 0
2026-01-13T20:40:35-05:00 | cat outputs/manifest.json | exit 0
2026-01-13T20:40:43-05:00 | cat <<'EOF' >> docs/CHANGELOG.md | exit 0
2026-01-13T20:41:23-05:00 | sed -n '1,200p' src/ena/io.py | exit 0
2026-01-13T20:41:38-05:00 | mkdir -p experiments/X01_strict_practice_any/... && init notes.md | exit 0
2026-01-13T20:42:53-05:00 | Rscript R/02_logit_practices.R | tee experiments/X01_strict_practice_any/logs/before.log | exit 0
2026-01-13T20:43:01-05:00 | cp outputs/tables/04_logit_main.csv ... experiments/X01_strict_practice_any/key_outputs_before/ | exit 0
2026-01-13T20:44:53-05:00 | X01 after-run: rebuild model data + logit | exit 0
2026-01-13T20:45:00-05:00 | cp outputs/tables/04_logit_main.csv ... experiments/X01_strict_practice_any/key_outputs_after/ | exit 0
2026-01-13T20:45:09-05:00 | ./venv/bin/python - <<'PY' (compare logit main before/after) | exit 0
2026-01-13T20:45:16-05:00 | ./venv/bin/python - <<'PY' (logit main before/after details) | exit 0
2026-01-13T20:45:26-05:00 | ./venv/bin/python - <<'PY' (practice_any mean after strict) | exit 0
2026-01-13T20:45:37-05:00 | ./venv/bin/python - <<'PY' (crosstab strict) | exit 0
2026-01-13T20:47:19-05:00 | X01 revert-run: rebuild model data + logit | exit 0
2026-01-13T20:47:39-05:00 | cat <<'EOF' > experiments/X01_strict_practice_any/notes.md | exit 0
2026-01-13T20:47:45-05:00 | cat <<'EOF' >> docs/CHANGELOG.md | exit 0
2026-01-13T20:48:06-05:00 | mkdir -p experiments/X02_standardize_sfa_z/... && init notes.md | exit 0
2026-01-13T20:49:59-05:00 | Rscript R/01_sfa_main.R | tee experiments/X02_standardize_sfa_z/logs/before.log | exit 0
2026-01-13T20:50:08-05:00 | cp outputs/tables/02_sfa_main.csv ... experiments/X02_standardize_sfa_z/key_outputs_before/ | exit 0
2026-01-13T20:53:09-05:00 | Rscript R/01_sfa_main.R | tee experiments/X02_standardize_sfa_z/logs/after.log | exit 0
2026-01-13T20:53:15-05:00 | cp outputs/tables/02_sfa_main.csv ... experiments/X02_standardize_sfa_z/key_outputs_after/ | exit 0
2026-01-13T20:53:25-05:00 | ./venv/bin/python - <<'PY' (SFA before/after terms) | exit 0
2026-01-13T20:53:33-05:00 | ./venv/bin/python - <<'PY' (SFA Z estimates before/after) | exit 0
2026-01-13T20:53:45-05:00 | rg -n "diversificacion_area_std|diversif_mediano_std|diversif_grande_std|diversif_alt_std|diversif_alt2_std" R/01_sfa_main.R | exit 0
2026-01-13T20:56:23-05:00 | Rscript R/01_sfa_main.R | tee experiments/X02_standardize_sfa_z/logs/revert.log | exit 0
2026-01-13T20:56:34-05:00 | cat <<'EOF' > experiments/X02_standardize_sfa_z/notes.md | exit 0
2026-01-13T20:56:44-05:00 | cat <<'EOF' >> docs/CHANGELOG.md | exit 0
2026-01-13T20:57:04-05:00 | sed -n '40,120p' docs/DEEP_AUDIT_REPORT.md | exit 0
2026-01-13T20:57:27-05:00 | sed -n '52,90p' docs/DEEP_AUDIT_REPORT.md | exit 0
2026-01-13T20:57:49-05:00 | ./venv/bin/python src/report/build_report.py | exit 0
2026-01-13T20:58:18-05:00 | rg -n --pcre2 '[^\x00-\x7F]' ... | exit 0
2026-01-13T20:58:47-05:00 | ./venv/bin/python - <<'PY' (ascii normalize docs/notes) | exit 0
2026-01-13T20:58:54-05:00 | rg -n --pcre2 '[^\x00-\x7F]' ... | exit 1
2026-01-13T20:59:01-05:00 | sed -n '1,120p' docs/SFA_INTERPRETATION_AUDIT.md | exit 0
2026-01-13T20:59:08-05:00 | sed -n '1,120p' docs/DEEP_AUDIT_REPORT.md | exit 0
2026-01-13T20:59:25-05:00 | sed -n '1,120p' docs/VARIABLE_DEFINITIONS_AUDIT.md | exit 0
2026-01-13T20:59:32-05:00 | sed -n '1,120p' docs/INTUITION_VS_RESULTS.md | exit 0
2026-01-13T20:59:40-05:00 | sed -n '1,200p' outputs/plots/00_index/plot_manifest.md | exit 0
2026-01-13T20:59:48-05:00 | sed -n '1,160p' docs/ERROR_LEDGER.md | exit 0
