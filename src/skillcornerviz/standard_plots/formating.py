# Compatibility shim — the canonical module is formatting.py (single 't' was a typo).
from skillcornerviz.standard_plots.formatting import (  # noqa: F401
    standard_ax_formating,
    prep_label_for_radar,
    simplify_label,
)
