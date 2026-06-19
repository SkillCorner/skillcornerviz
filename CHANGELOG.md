# Changelog

All notable changes to skillcornerviz are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [1.2.2] – 2026-06-19

### Changed
- Updated README: contact email, example snippets for `narrative_ranking_plot` and `table_grid`, example images, file structure.
- Added GitHub Actions workflow for automatic PyPI publishing on version tag push.

---

## [1.2.1] – 2026-06-19

### Changed
- `table_grid`: renamed `row_id_col` → `data_point_id` for API consistency with other plot functions.

### Added
- `table_grid`: new `highlight_group` parameter to filter displayed rows to a shortlist of `data_point_id` values.

---

## [1.2.0] – 2026-04-24

### Added
- `narrative_ranking_plot.plot_ranking` — ranked player × metric grid with percentile colour coding and optional circle markers.
- `zscore_dotplot.plot_zscore_dotplot` — horizontal dot plot showing z-score positions across grouped metrics with population range bars.
- `table_grid.plot_table_grid` — seaborn heatmap grid for z-scored metrics with optional column-gap dividers and a labelled colour bar.

### Changed
- Migrated font stack from Roboto to **Shentox** across all plots.
- Centralised font loading into `utils/_fonts.py` (`load_shentox_fonts`); fonts are registered once per process, preventing repeated re-registration on every import.
- Dropped `setup.py`; packaging is now fully declared in `pyproject.toml`.
- `package-data` now explicitly ships `resources/Shentox/*.otf` and `resources/Roboto/*.ttf` in the built wheel.
- Removed `setuptools` from runtime `dependencies` (it is a build tool only).
- Minimum Python version set to 3.9 (`requires-python = ">=3.9"`).

### Fixed
- `swarm_violin_plot` now accepts a `dark_mode` parameter; text, spines, and highlight colours all respect dark mode.
- `scatter_plot`: bitwise `&` replaced with `and` in highlight-group filter; invalid escape `"\ "` replaced with `r"\ "`.
- `summary_table`: ordinal suffixes (1st/2nd/3rd/11th/12th/13th) now use correct edge-case logic.
- `skillcorner_utils.merge_sc_dataframes`: fixed incorrect merge behaviour when list contained fewer than three DataFrames.
- `skillcorner_utils`: `get_player_age`, `add_percentile_values`, and `add_data_point_id` now return the modified DataFrame.
- `skillcorner_physical_utils`: `add_p60_bip`, `add_p30_tip`, `add_p30_otip` now return the modified DataFrame.
- `constants.py`: corrected `'Toemporada'` → `'Temporada'` in Portuguese strings.
- `formating.py` spelling: canonical module is now `formatting.py`; old name kept as a re-export shim for backwards compatibility.
- Font loading switched from deprecated `pkg_resources` to `importlib.resources.files()`.
- Author name typo fixed: "Micheal" → "Michael" in package metadata.

---

## [1.1.1] – 2024 (prior release)

### Changed
- Updated physical metric naming to match SkillCorner v3 API (`minutes_full_all`, `metric_full_tip`, etc.).

### Fixed
- Rounding error in `summary_table` rank display.
- README example image links updated.

---

## [1.0.8] – 2024 (prior release)

### Added
- GitHub repository link added to package metadata.

---

## [1.0.0] – 2024 (initial release)

- Initial public release with `bar_plot`, `scatter_plot`, `radar_plot`, `summary_table`, and `swarm_violin_plot`.
- Utility modules: `skillcorner_game_intelligence_utils`, `skillcorner_physical_utils`, `skillcorner_utils`.
