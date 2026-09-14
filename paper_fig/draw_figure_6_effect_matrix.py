"""Render only Figure 6 from saved primary paired effects.

Usage: python -B draw_figure_6_effect_matrix.py
Dependencies: matplotlib, numpy, pandas, and a pandas Parquet engine.
No experiment modules are imported or executed. Missing standardised effects
stay NaN; the shared colour scale uses the full finite point-effect range.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import numpy as np
import pandas as pd


SCENARIOS = ("schelling", "deffuant")
SCALES = ("micro", "meso", "macro")
SCALE_CODES = {"micro": "Mi", "meso": "Me", "macro": "Ma"}
STEM = "figure_6_effect_matrix"
INPUTS = (
    "analysis/paired_effects.parquet",
    "representation/indicators_frozen.json",
    "config/experiment_config.snapshot.json",
)
EFFECT = "cumulative_effect_standardised"
LOW = "cumulative_ci_low_standardised"
HIGH = "cumulative_ci_high_standardised"
COLOURS = {"ink": "#20282E", "grey": "#6F777B", "paper": "white",
           "na_slash": "#B8BDC1"}
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 7, "axes.linewidth": 1.0, "axes.edgecolor": COLOURS["ink"],
    "axes.facecolor": COLOURS["paper"], "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": COLOURS["ink"], "xtick.color": COLOURS["ink"], "ytick.color": COLOURS["ink"],
    "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.width": 0.9, "ytick.major.width": 0.9, "legend.frameon": False,
    "svg.fonttype": "none", "pdf.fonttype": 42, "svg.hashsalt": "camo-paper-figure-6",
    "savefig.transparent": False, "figure.facecolor": COLOURS["paper"],
    "savefig.facecolor": COLOURS["paper"],
})
# Unchanged diverging colour anchors from the original paper heatmap.
DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "camo_frosted_diverging", ["#2B5D7E", "#AFC6D2", "#F5F0E6", "#D9A39A", "#B84A3C"])
# Match the zero colour only at the rendering layer; the masked values stay NaN.
DIVERGING_CMAP.set_bad(DIVERGING_CMAP(0.5))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_inputs(run: Path) -> tuple[pd.DataFrame, dict, float]:
    effects = pd.read_parquet(run / INPUTS[0])
    indicators = json.loads((run / INPUTS[1]).read_text(encoding="utf-8"))
    config = json.loads((run / INPUTS[2]).read_text(encoding="utf-8"))
    confidence = float(config["intervention"]["confidence_level"])
    if set(effects.evaluation_track) != {"primary_discovery"}:
        raise ValueError("Unexpected evaluation track in the primary paired-effects file")
    if set(effects.scenario) != set(SCENARIOS) or set(effects.scale) != set(SCALES):
        raise ValueError("Unexpected scenario or scale set; refusing to omit observations")
    keys = ["scenario", "parameter", "direction", "node_id"]
    if effects[keys].isna().any().any() or effects.duplicated(keys).any():
        raise ValueError("Missing or duplicate paired-effect keys")
    if not effects.direction.isin(["minus", "plus"]).all():
        raise ValueError("Unexpected intervention direction")
    values = effects[EFFECT].to_numpy(float)
    if np.isinf(values).any():
        raise ValueError("Infinite effect encountered; cannot define a finite full-range colour scale")
    np.testing.assert_allclose(values, effects.cumulative_effect.to_numpy(float), equal_nan=True)
    missing = effects[EFFECT].isna()
    if not effects.loc[missing, "baseline_sd"].eq(0).all():
        raise ValueError("An undefined effect has a different cause; revise the figure-specific missing-value caption")
    low, high = effects[LOW], effects[HIGH]
    if not low.isna().equals(high.isna()) or (low > high).any():
        raise ValueError("Incomplete or reversed saved effect interval")
    flags = effects.significant.astype(str)
    if not flags.isin(["True", "False"]).all():
        raise ValueError("Unexpected saved significance flags")
    effects = effects.copy()
    effects["saved_significant"] = flags.eq("True")
    effects["ci_excludes_zero"] = (low > 0) | (high < 0)
    # Preserve the original dot selection, including all original criteria.
    # Do not replace saved scientific flags by a newly computed interval-only rule.
    if (effects.saved_significant & (~effects.ci_excludes_zero | missing)).any():
        raise ValueError("Saved significance does not satisfy the displayed interval statement")
    names = {(scenario, item["id"]): {"name": item["semantic_name"], "scale": item["scale"]}
             for scenario, value in indicators["scenarios"].items() for item in value["indicators"]}
    for item in effects.itertuples(index=False):
        if names[(item.scenario, item.node_id)]["scale"] != item.scale:
            raise ValueError("Frozen indicator scale differs from paired-effects scale")
    return effects, names, confidence


def panel_data(effects: pd.DataFrame, names: dict, scenario: str) -> tuple:
    subset = effects[effects.scenario == scenario]
    conditions = subset[["parameter", "direction"]].drop_duplicates().sort_values(["parameter", "direction"])
    columns = subset[["node_id", "scale"]].drop_duplicates().copy()
    if columns.node_id.duplicated().any():
        raise ValueError("One indicator appears under multiple scales")
    columns["order"] = columns.scale.map({scale: index for index, scale in enumerate(SCALES)})
    columns = columns.sort_values(["order", "node_id"])
    row_keys = list(conditions.itertuples(index=False, name=None))
    node_ids = columns.node_id.tolist()
    expected = pd.MultiIndex.from_tuples(
        [(parameter, direction, node) for parameter, direction in row_keys for node in node_ids],
        names=["parameter", "direction", "node_id"])
    lookup = subset.set_index(["parameter", "direction", "node_id"])
    if len(lookup) != len(expected) or not expected.isin(lookup.index).all():
        raise ValueError("Incomplete condition-by-indicator matrix; missing rows are not zero effects")
    cells = lookup.loc[expected].reset_index().copy()
    matrix = cells[EFFECT].to_numpy(float).reshape(len(row_keys), len(node_ids))
    significant = cells.saved_significant.to_numpy(bool).reshape(matrix.shape)
    counters = {scale: 0 for scale in SCALES}
    codebook = []
    for column, item in enumerate(columns.itertuples(index=False)):
        counters[item.scale] += 1
        codebook.append({"scenario": scenario, "column": column, "node_id": item.node_id,
            "scale": item.scale, "code": f"{SCALE_CODES[item.scale]}{counters[item.scale]:02d}",
            "semantic_name": names[(scenario, item.node_id)]["name"]})
    codes = {row["node_id"]: row["code"] for row in codebook}
    cells["row"] = np.repeat(np.arange(len(row_keys)), len(node_ids))
    cells["column"] = np.tile(np.arange(len(node_ids)), len(row_keys))
    cells["code"] = cells.node_id.map(codes)
    cells["display_na"] = cells[EFFECT].isna()
    cells["display_significance_dot"] = cells.saved_significant & ~cells.display_na
    return row_keys, columns, matrix, significant, cells, codebook


def render(run: Path, output: Path) -> dict:
    if output == run or run in output.parents:
        raise ValueError("Figure output must be outside the archived run")
    before = {name: sha256(run / name) for name in INPUTS}
    effects, names, confidence = load_inputs(run)
    finite = effects.loc[np.isfinite(effects[EFFECT]), EFFECT].to_numpy(float)
    if not len(finite):
        raise ValueError("No defined standardised effects")
    max_abs_effect = float(np.abs(finite).max())
    if max_abs_effect <= 0:
        raise ValueError("All effects are zero; a nondegenerate full-range colour scale is undefined")
    norm = TwoSlopeNorm(vmin=-max_abs_effect, vcenter=0.0, vmax=max_abs_effect)
    fig, axes = plt.subplots(2, 1, figsize=(7.20, 4.85))
    images, plotted_cells, codebooks = [], [], []
    audit = {}
    for index, scenario in enumerate(SCENARIOS):
        ax = axes[index]
        letter = "ab"[index]
        row_keys, columns, matrix, significant, cells, codebook = panel_data(effects, names, scenario)
        plotted_cells.append(cells)
        codebooks.extend(codebook)
        missing = np.isnan(matrix)
        image = ax.imshow(np.ma.array(matrix, mask=missing), cmap=DIVERGING_CMAP, norm=norm,
                          aspect="auto", interpolation="nearest", gid=f"{letter}-effect-heatmap")
        images.append(image)
        np.testing.assert_array_equal(np.ma.getmaskarray(image.get_array()), missing)
        np.testing.assert_allclose(image.get_array().data, matrix, equal_nan=True)
        for row, column in zip(*np.where(missing)):
            ax.text(column + 0.39, row - 0.40, "/", ha="right", va="top", fontsize=4.0,
                color=COLOURS["na_slash"], zorder=4,
                gid=f"{letter}-na-{row}-{column}-slash")
        ax.set_yticks(range(len(row_keys)),
            [f"{parameter.replace('_', ' ').capitalize()} {'+' if direction == 'plus' else '−'}"
             for parameter, direction in row_keys], fontsize=6.0)
        ax.set_xticks(range(len(codebook)), [item["code"] for item in codebook], rotation=90, fontsize=6.0)
        for row, column in zip(*np.where(significant & ~missing)):
            marker_colour = COLOURS["paper"] if abs(matrix[row, column]) > 0.56 * max_abs_effect else COLOURS["ink"]
            ax.scatter(column, row, s=3.2, color=marker_colour, linewidth=0, zorder=3,
                       gid=f"{letter}-significant-{row}-{column}")
        counts = columns.groupby("scale", sort=False).size().to_dict()
        boundary = 0
        for scale in SCALES:
            count = int(counts.get(scale, 0))
            if not count:
                continue
            ax.text(boundary + (count - 1) / 2, 1.035, f"{scale.capitalize()}  n={count}",
                transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=6.2,
                fontweight="bold", color=COLOURS["ink"])
            boundary += count
            if boundary < len(columns):
                ax.axvline(boundary - 0.5, color=COLOURS["paper"], lw=2.0)
                ax.axvline(boundary - 0.5, color=COLOURS["ink"], lw=0.45, alpha=0.45)
        ax.set_title(f"{scenario.capitalize()} paired cumulative effects", fontsize=7.5, pad=18)
        ax.tick_params(length=3.0, width=0.9, labelsize=6.2, pad=2)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.8)
        ax.text(-0.11, 1.06, letter, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top")
        audit[letter] = {"scenario": scenario, "shape": list(matrix.shape),
            "scale_counts": {scale: int(counts[scale]) for scale in SCALES},
            "na_count": int(missing.sum()), "significance_dot_count": int((significant & ~missing).sum()),
            "na_cells": cells.loc[cells.display_na, ["parameter", "direction", "node_id", "code", "row", "column"]].to_dict("records")}
    fig.subplots_adjust(left=0.205, right=0.905, bottom=0.09, top=0.94, hspace=0.47)
    colorbar_axis = fig.add_axes([0.923, 0.13, 0.014, 0.74])
    colorbar = fig.colorbar(images[-1], cax=colorbar_axis)
    ticks = np.linspace(-max_abs_effect, max_abs_effect, 5)
    colorbar.set_ticks(ticks, labels=["0" if value == 0 else f"{value:.2f}" for value in ticks])
    colorbar.set_label("Standardised cumulative effect", fontsize=6.5)
    colorbar.ax.tick_params(labelsize=6.0, width=0.75, length=2.6)
    colorbar.ax.set_title(f"● {confidence:.0%} CI\nexcludes zero", fontsize=5.8, color=COLOURS["grey"], pad=5)
    if not all(image.norm is norm for image in images) or colorbar.norm is not norm:
        raise AssertionError("Both panels and the colourbar must share the same normalisation")
    np.testing.assert_allclose(norm([-max_abs_effect, 0, max_abs_effect]), [0, 0.5, 1])
    fig.canvas.draw()
    output.mkdir(parents=True, exist_ok=True)
    exports = []
    for extension in ("svg", "png"):
        path = output / f"{STEM}.{extension}"
        fig.savefig(path, format=extension, dpi=300, bbox_inches="tight", pad_inches=0.03)
        exports.append(path)
    plt.close(fig)
    source_dir, qa_dir = output / "source_data", output / "qa"
    source_dir.mkdir(exist_ok=True)
    qa_dir.mkdir(exist_ok=True)
    cell_table = pd.concat(plotted_cells, ignore_index=True)
    cell_table.to_csv(source_dir / "figure_6_plotted_cells.tsv", sep="\t", index=False, na_rep="NA")
    pd.DataFrame(codebooks).to_csv(source_dir / "figure_6_indicator_codebook.tsv", sep="\t", index=False)
    caption = (
        "Figure 6. Standardised paired cumulative effects for Schelling (a) and Deffuant (b). "
        "Rows denote saved parameter-direction conditions; columns are grouped into Micro, Meso and Macro. "
        "Mi, Me and Ma codes number indicators in node-ID order within each scale and scenario; the full "
        "frozen semantic-name mapping is supplied in source_data/figure_6_indicator_codebook.tsv. "
        "Both panels share the original diverging palette and one colourbar centred on zero. "
        f"The limits are [−{max_abs_effect:.10f}, +{max_abs_effect:.10f}], calculated from the maximum "
        "absolute finite cumulative_effect_standardised across both scenarios, without percentile "
        "clipping or saturation of any defined point estimate. "
        f"Dots preserve the saved significant flags, all of which satisfy {confidence:.0%} CI exclusion "
        "of zero as well as the run's original additional significance criteria. These flags are not "
        "recomputed from interval signs alone. In this figure, slash-marked cells indicate undefined "
        "standardized effects because baseline variance is zero. Undefined cells use the same neutral "
        "colour as zero, with a small, light-grey / in the upper-right corner; their data remain NaN "
        "and they receive no significance dot. "
        "No paired effects, confidence intervals, significance decisions or experimental settings are altered.\n\n"
        "The full plotted cells and their saved values are supplied in source_data/figure_6_plotted_cells.tsv.\n\n"
        "Inputs:\n" + "".join(f"- `{name}`\n" for name in INPUTS)
    )
    (output / "figure_6_caption.md").write_text(caption, encoding="utf-8")
    after = {name: sha256(run / name) for name in INPUTS}
    if before != after:
        raise RuntimeError("A source artifact changed during rendering")
    report = {"status": "passed", "source_run": str(run), "source_sha256": before,
        "source_rows": len(effects), "finite_effect_count": len(finite),
        "undefined_effect_count": int(effects[EFFECT].isna().sum()),
        "actual_finite_range": [float(finite.min()), float(finite.max())],
        "max_abs_effect": max_abs_effect, "colour_limits": [-max_abs_effect, max_abs_effect],
        "normalisation_center": 0.0, "shared_normalisation": True, "shared_colourbar_count": 1,
        "percentile_clipping": False, "undefined_as_zero": False,
        "undefined_display": "zero-colour background with a small light-grey upper-right slash",
        "undefined_rgba": DIVERGING_CMAP.get_bad().tolist(), "zero_rgba": list(DIVERGING_CMAP(norm(0.0))),
        "significance_rule": "unchanged saved significant flags", "saved_confidence_level": confidence,
        "significance_dot_count": int(effects.saved_significant.sum()),
        "saved_ci_excludes_zero_count": int(effects.ci_excludes_zero.sum()),
        "panels": audit, "input_unchanged": True, "experiment_recalculation": False,
        "script_sha256": sha256(Path(__file__)), "outputs": {path.name: sha256(path) for path in exports}}
    (qa_dir / "figure_6_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path,
        default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = render(args.run.resolve(), args.output_dir.resolve())
    print(json.dumps({name: result[name] for name in
        ("status", "finite_effect_count", "undefined_effect_count", "colour_limits", "significance_dot_count", "outputs")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
