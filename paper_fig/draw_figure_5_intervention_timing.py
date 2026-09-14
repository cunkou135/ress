"""Render Figure 5 from saved primary results; never run experimental code.

Usage: python -B draw_figure_5_intervention_timing.py
Dependencies: matplotlib, numpy, pandas, and a pandas Parquet engine.
The original Figure 5 typography, blue/red scale colours, line styles,
markers, interval opacity and 2-by-2 arrangement are retained on white.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


SCENARIOS = ("schelling", "deffuant")
SCALES = ("micro", "meso", "macro")
STEM = "figure_5_intervention_timing"
INPUTS = (
    "analysis/representative_path_selection.json",
    "analysis/path_intervention_classification.csv",
    "analysis/holdout_path_confirmation.csv",
    "analysis/path_timing_summary.csv",
    "analysis/effect_curves.parquet",
    "representation/indicators_frozen.json",
)
COLOURS = {"micro": "#2B5D7E", "meso": "#2B5D7E", "macro": "#B84A3C",
           "grey": "#6F777B", "ink": "#20282E"}
LINESTYLES = {"micro": "-", "meso": (0, (4, 2)), "macro": "-"}
DELAY_SEGMENTS = (("micro", "meso"), ("meso", "macro"))
DELAY_STYLES = (
    {"color": COLOURS["micro"], "marker": "o", "ms": 7.0,
     "mfc": "white", "mec": COLOURS["micro"], "mew": 1.1},
    {"color": COLOURS["macro"], "marker": "s", "ms": 3.2,
     "mfc": COLOURS["macro"], "mec": COLOURS["macro"], "mew": 1.0},
)
# These abbreviations affect text only; membership and all numbers are read.
PARAMETER_LABELS = {"tolerance": "Tol", "confidence_bound": "CB"}
MACRO_LABELS = {
    "macro_global_spatial_neighbor_similarity": "spatial sim.",
    "macro_global_connected_components": "components",
    "macro_global_moved_fraction": "relocation",
    "macro_network_assortativity": "assortativity",
    "macro_opinion_global_variance": "global var.",
}
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 7, "axes.linewidth": 1.0, "axes.edgecolor": COLOURS["ink"],
    "axes.facecolor": "white", "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": COLOURS["ink"], "xtick.color": COLOURS["ink"],
    "ytick.color": COLOURS["ink"], "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.width": 0.9, "ytick.major.width": 0.9, "legend.frameon": False,
    "svg.fonttype": "none", "pdf.fonttype": 42, "svg.hashsalt": "camo-paper-figure-5",
    "figure.facecolor": "white", "savefig.facecolor": "white", "savefig.transparent": False,
})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def style_axes(ax, letter: str, *, grid: bool = False) -> None:
    ax.spines["left"].set_linewidth(1.1)
    ax.spines["bottom"].set_linewidth(1.1)
    ax.tick_params(length=3.0, width=0.9, labelsize=6.2, pad=2)
    if grid:
        ax.grid(axis="both", color="#D7D8D4", lw=0.5, ls="--", alpha=0.45, zorder=0)
    ax.text(-0.11, 1.06, letter, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top")


def short_path_label(path, node_names: dict) -> str:
    parameter = PARAMETER_LABELS.get(path.parameter, path.parameter.replace("_", " "))
    direction = {"minus": "−", "plus": "+"}[path.direction]
    outcome = MACRO_LABELS.get(path.macro, node_names[(path.scenario, path.macro)])
    return f"{parameter}{direction} | {outcome}"


def inter_scale_delays(group: pd.DataFrame) -> list[dict]:
    """Saved-onset differences and segment coordinates relative to Micro onset."""
    onsets = group.set_index("scale")["onset_time"]
    micro_onset = float(onsets.loc["micro"])
    records = []
    for source_scale, target_scale in DELAY_SEGMENTS:
        source_onset = float(onsets.loc[source_scale])
        target_onset = float(onsets.loc[target_scale])
        records.append({"source_scale": source_scale, "target_scale": target_scale,
            "source_onset": source_onset, "target_onset": target_onset,
            "delay": target_onset - source_onset, "micro_onset": micro_onset,
            "display_start_x": source_onset - micro_onset,
            "display_end_x": target_onset - micro_onset})
    return records


def draw_onset_labels(ax, grouped_onsets: dict, letter: str) -> list[dict]:
    """Label every saved onset; stagger nearby text across the upper plot edge."""
    renderer = ax.figure.canvas.get_renderer()
    font = FontProperties(family=mpl.rcParams["font.family"], size=5.8)
    pixels_per_point = ax.figure.dpi / 72.0
    previous_right = -math.inf
    records = []
    for onset, scales in sorted(grouped_onsets.items()):
        label = "/".join(scale.capitalize() for scale in scales)
        colours = {COLOURS[scale] for scale in scales}
        colour = COLOURS[scales[0]] if len(colours) == 1 else COLOURS["grey"]
        anchor_x = ax.get_xaxis_transform().transform((onset, 1.01))[0]
        label_left = anchor_x + 3 * pixels_per_point
        crowded = label_left < previous_right + 4 * pixels_per_point
        width, _, _ = renderer.get_text_width_height_descent(label, font, ismath=False)
        if not crowded:
            previous_right = label_left + width
        label_y = 0.995 if crowded else 1.01
        ax.annotate(label, xy=(onset, label_y), xycoords=ax.get_xaxis_transform(),
            xytext=(3, 0), textcoords="offset points", ha="left", va="top" if crowded else "bottom",
            fontproperties=font, color=colour,
            gid=f"{letter}-{'-'.join(scales)}-onset-label")
        records.append({"time": onset, "label": label, "scales": scales,
                        "text_offset_points": 3, "text_y_axes": label_y, "onset_line_x": onset})
    return records


def load_inputs(run: Path) -> dict:
    selection = json.loads((run / INPUTS[0]).read_text(encoding="utf-8"))
    classification = pd.read_csv(run / INPUTS[1])
    holdout = pd.read_csv(run / INPUTS[2])
    timing = pd.read_csv(run / INPUTS[3])
    curves = pd.read_parquet(run / INPUTS[4])
    indicators = json.loads((run / INPUTS[5]).read_text(encoding="utf-8"))
    if classification.duplicated(["scenario", "path_id"]).any():
        raise ValueError("Duplicate primary path classifications")
    # Final saved classification is the only scientific path inclusion rule.
    supported = classification[classification.path_classification == "supported"].copy()
    if set(supported.scenario) != set(SCENARIOS):
        raise ValueError("Supported scenario set differs from the requested two-panel rows")
    timing = timing[timing.evaluation_track == "primary_discovery"].copy()
    curves = curves[curves.evaluation_track == "primary_discovery"].copy()
    node_names = {(scenario, node["id"]): node["semantic_name"]
                  for scenario, value in indicators["scenarios"].items()
                  for node in value["indicators"]}
    confirmed = set(zip(
        holdout.loc[holdout.holdout_confirmed.astype(str) == "True", "scenario"],
        holdout.loc[holdout.holdout_confirmed.astype(str) == "True", "path_id"],
    ))
    representatives = {}
    timing_groups = {}
    displayed_curves = []
    path_records = []
    for scenario in SCENARIOS:
        # Preserve the run's saved representative, including its holdout preference.
        saved = selection["scenarios"][scenario]
        path_id = saved["path_id"]
        paths = supported[supported.scenario == scenario].sort_values("path_id")
        if path_id not in set(paths.path_id):
            raise ValueError(f"Saved representative is not primary supported: {scenario}/{path_id}")
        if saved.get("evidence_scope") == "holdout_confirmed" and (scenario, path_id) not in confirmed:
            raise ValueError("Saved representative holdout scope disagrees with confirmation table")
        representatives[scenario] = {"path_id": path_id,
            "holdout_confirmed": (scenario, path_id) in confirmed,
            "saved_evidence_scope": saved.get("evidence_scope")}
        labels = []
        for path in paths.itertuples(index=False):
            key = (scenario, path.path_id)
            group = timing[(timing.scenario == scenario) & (timing.path_id == path.path_id)]
            if len(group) != 3 or set(group.scale) != set(SCALES):
                raise ValueError(f"Missing or duplicate scale timing rows for {key}")
            group = group.set_index("scale").loc[list(SCALES)].reset_index()
            for item in group.itertuples(index=False):
                if (item.parameter, item.direction, item.node_id) != (
                        path.parameter, path.direction, getattr(path, item.scale)):
                    raise ValueError(f"Timing/path identity mismatch: {key}/{item.scale}")
            intervals = group[["onset_time", "onset_ci_low", "onset_ci_high"]].to_numpy(float)
            if not np.isfinite(intervals[:, 0]).all() or np.any(intervals[:, 0] < 0):
                raise ValueError(f"Missing onset evidence for a supported path: {key}")
            available = np.isfinite(intervals[:, 1:]).all(axis=1)
            saved_intervals = intervals[available]
            if (np.any(saved_intervals[:, 1] < 0)
                    or np.any(saved_intervals[:, 1] > saved_intervals[:, 0])
                    or np.any(saved_intervals[:, 0] > saved_intervals[:, 2])):
                raise ValueError(f"Saved onset interval does not contain its onset: {key}")
            # No onset-order/significance filter: these checks must not redefine support.
            timing_groups[key] = group
            label = short_path_label(path, node_names)
            labels.append(label)
            record = {"scenario": scenario, "path_label": label, "path_id": path.path_id,
                "parameter": path.parameter, "direction": path.direction,
                "path_classification": path.path_classification,
                "holdout_confirmed": key in confirmed, "representative": path.path_id == path_id}
            for scale in SCALES:
                item = group[group.scale == scale].iloc[0]
                record[scale] = getattr(path, scale)
                record[f"{scale}_semantic_name"] = node_names[(scenario, getattr(path, scale))]
                for field in ("onset_time", "onset_ci_low", "onset_ci_high"):
                    record[f"{scale}_{field}"] = float(item[field])
            path_records.append(record)
            if path.path_id != path_id:
                continue
            representatives[scenario]["path_label"] = label
            for scale in SCALES:
                selected = curves[(curves.scenario == scenario) & (curves.parameter == path.parameter)
                    & (curves.direction == path.direction) & (curves.node_id == getattr(path, scale))
                    & curves.time.between(0, 30)].sort_values("time").copy()
                if selected.empty or selected.time.duplicated().any():
                    raise ValueError(f"Missing or duplicate representative curve: {key}/{scale}")
                if not selected.centre_statistic.eq("mean").all():
                    raise ValueError("Saved curve centre statistic is not mean")
                np.testing.assert_allclose(selected["mean"], selected.mean_standardised, equal_nan=True)
                values = selected[["mean", "ci_low", "ci_high"]].to_numpy(float)
                if not np.isfinite(values).all() or np.any(values[:, 1] > values[:, 2]):
                    raise ValueError("Invalid saved effect curve or interval")
                selected["path_id"], selected["scale"] = path_id, scale
                displayed_curves.append(selected)
        if len(labels) != len(set(labels)):
            raise ValueError("Ambiguous display labels; expand figure-specific label helper")
    return {"representatives": representatives, "selection_rule": selection.get("selection_rule"),
            "path_records": pd.DataFrame(path_records), "timing": timing_groups,
            "curves": pd.concat(displayed_curves, ignore_index=True)}


def render(run: Path, output: Path) -> dict:
    if output == run or run in output.parents:
        raise ValueError("Figure output must be outside the archived run")
    before = {name: sha256(run / name) for name in INPUTS}
    data = load_inputs(run)
    fig, axes = plt.subplots(2, 2, figsize=(7.20, 4.95),
                             gridspec_kw={"width_ratios": [44, 56]})
    fig.subplots_adjust(left=0.10, right=0.99, bottom=0.12, top=0.88,
                        wspace=0.31, hspace=0.56)
    handles = [Line2D([0], [0], ls="-", lw=2.6, **style,
               label=f"{source.capitalize()}→{target.capitalize()} delay")
               for (source, target), style in zip(DELAY_SEGMENTS, DELAY_STYLES)]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.54, 0.995),
               fontsize=6.5, ncol=2, handlelength=2.6, columnspacing=2.0, handletextpad=0.6,
               frameon=True, facecolor="white", edgecolor="#D7D8D4", framealpha=1.0)
    audit = {}
    delay_records = []
    for row, scenario in enumerate(SCENARIOS):
        representative = data["representatives"][scenario]
        path_id = representative["path_id"]
        group = data["timing"][(scenario, path_id)]
        ax = axes[row, 0]
        letter = "ac"[row]
        bounds = [0.0]
        curve_audit = {}
        grouped_onsets = {}
        for scale in SCALES:
            curve = data["curves"][(data["curves"].scenario == scenario) & (data["curves"].scale == scale)]
            x, mean, low, high = (curve[name].to_numpy(float) for name in ("time", "mean", "ci_low", "ci_high"))
            line, = ax.plot(x, mean, color=COLOURS[scale], lw=2.6, ls=LINESTYLES[scale],
                solid_capstyle="round", label=scale.capitalize(), gid=f"{letter}-{scale}-mean-effect")
            ax.fill_between(x, low, high, color=COLOURS[scale], alpha=0.10, linewidth=0,
                            gid=f"{letter}-{scale}-saved-effect-interval")
            onset = float(group.loc[group.scale == scale, "onset_time"].iloc[0])
            grouped_onsets.setdefault(onset, []).append(scale)
            bounds.extend(low.tolist() + high.tolist() + mean.tolist())
            np.testing.assert_array_equal(line.get_ydata(), mean)
            curve_audit[scale] = {"point_count": len(x), "first_time": float(x.min()),
                                 "last_time": float(x.max()), "onset": onset}
        for onset, scales in grouped_onsets.items():
            colours = {COLOURS[scale] for scale in scales}
            colour = COLOURS[scales[0]] if len(colours) == 1 else COLOURS["grey"]
            ax.axvline(onset, color=colour, lw=1.1, ls=(0, (2, 2)),
                       gid=f"{letter}-{'-'.join(scales)}-onset", zorder=3)
        lower, upper = min(bounds), max(bounds)
        padding = max(0.08 * (upper - lower), 0.08)
        ax.set_ylim(lower - padding, upper + padding)
        ax.axhline(0, color=COLOURS["grey"], lw=0.85)
        ax.set_xlim(0, 30)
        ax.set_xticks([0, 10, 20, 30])
        ax.set_xlabel("Simulation time")
        ax.set_ylabel("Mean standardised paired effect")
        ax.set_title(f"{scenario.capitalize()} | Representative path response",
                     fontsize=7.2, fontweight="bold", pad=14)
        onset_labels = draw_onset_labels(ax, grouped_onsets, letter)
        legend = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3,
            fontsize=6.0, handlelength=3.8, columnspacing=1.4, handletextpad=0.6,
            borderaxespad=0, frameon=True, facecolor="white", edgecolor="#D7D8D4", framealpha=1.0)
        legend.get_frame().set_linewidth(0.6)
        style_axes(ax, letter, grid=True)
        audit[letter] = {"scenario": scenario, "representative_path": path_id,
                         "statistic": "mean", "curves": curve_audit,
                         "curve_legend_location": "centred below the panel", "onset_labels": onset_labels,
                         "unique_onset_lines": [{"time": time, "scales": scales}
                                                for time, scales in grouped_onsets.items()]}

        ax = axes[row, 1]
        letter = "bd"[row]
        paths = data["path_records"][data["path_records"].scenario == scenario]
        path_labels = []
        panel_delays = [0.0]
        for index, path in enumerate(paths.itertuples(index=False)):
            path_labels.append(path.path_label)
            group = data["timing"][(scenario, path.path_id)]
            delays = inter_scale_delays(group)
            np.testing.assert_equal(delays[0]["display_start_x"], 0.0)
            np.testing.assert_equal(delays[0]["display_end_x"], delays[1]["display_start_x"])
            for record, style in zip(delays, DELAY_STYLES):
                # A delay is a segment length, not an absolute horizontal position.
                # Coincident onsets retain exactly zero-length segments and no jitter.
                start, end = record["display_start_x"], record["display_end_x"]
                segment, = ax.plot([start, end], [index, index], color=style["color"],
                    ls="-", lw=2.6, solid_capstyle="round", zorder=2,
                    gid=f"{letter}-path-{index}-{record['source_scale']}-{record['target_scale']}-segment")
                np.testing.assert_array_equal(segment.get_xdata(), [start, end])
                np.testing.assert_allclose(end - start, record["delay"])
                delay_records.append({"panel": letter, "scenario": scenario, "path_id": path.path_id,
                    "path_label": path.path_label, **record,
                    "display_x": end, "display_y": index})
                panel_delays.extend([start, end])
            # Draw endpoints above both segments. Equal endpoints remain coincident;
            # the smaller Macro square fits inside the hollow blue Micro/Meso circle.
            for scale, x, style in (("micro", 0.0, DELAY_STYLES[0]),
                ("meso", delays[0]["display_end_x"], DELAY_STYLES[0]),
                ("macro", delays[1]["display_end_x"], DELAY_STYLES[1])):
                ax.plot([x], [index], ls="None", **style, zorder=3,
                        gid=f"{letter}-path-{index}-{scale}-relative-onset")
        lower, upper = min(panel_delays), max(panel_delays)
        span = max(upper - lower, 1.0)
        tick_step = max(1, math.ceil(span / 5))
        ax.set_xlim(lower - 0.06 * span, upper + 0.08 * span)
        ax.set_xticks(np.arange(math.floor(lower / tick_step) * tick_step,
                               upper + 0.01, tick_step))
        ax.set_yticks(np.arange(len(paths)), path_labels)
        ax.set_ylim(len(paths) - 0.48, -0.48)
        ax.set_xlabel("Time since Micro onset")
        ax.set_title(f"{scenario.capitalize()} | Supported-path propagation timelines",
                     fontsize=7.2, fontweight="bold", pad=14)
        ax.grid(axis="x", color="#D7D8D4", lw=0.5, ls="--", alpha=0.4, zorder=0)
        style_axes(ax, letter)
        for tick, record in zip(ax.get_yticklabels(), paths.itertuples(index=False)):
            tick.set_fontsize(5.8)
            if record.representative:
                tick.set_fontweight("bold")
        audit[letter] = {"scenario": scenario, "path_ids": paths.path_id.tolist(),
                         "path_count": len(paths), "x_jitter": False, "y_jitter": False,
                         "quantity": "onset time relative to Micro onset", "delay_count": 2 * len(paths),
                         "segment_coordinates": "Micro 0 to Meso; Meso to Macro, both relative to Micro onset",
                         "x_limits": list(ax.get_xlim())}
    fig.canvas.draw()
    widths = [ax.get_position().width for ax in axes[0]]
    column_width_fractions = [width / sum(widths) for width in widths]
    np.testing.assert_allclose(column_width_fractions, [0.44, 0.56])
    output.mkdir(parents=True, exist_ok=True)
    exports = []
    for extension in ("svg", "png"):
        target = output / f"{STEM}.{extension}"
        fig.savefig(target, format=extension, dpi=300, bbox_inches="tight", pad_inches=0.03)
        exports.append(target)
    plt.close(fig)
    source_dir, qa_dir = output / "source_data", output / "qa"
    source_dir.mkdir(exist_ok=True)
    qa_dir.mkdir(exist_ok=True)
    data["curves"].to_csv(source_dir / "figure_5_plotted_effect_curves.tsv", sep="\t", index=False)
    data["path_records"].to_csv(source_dir / "figure_5_supported_path_labels.tsv", sep="\t", index=False)
    pd.DataFrame(delay_records).to_csv(source_dir / "figure_5_plotted_delays.tsv", sep="\t", index=False)
    caption = (
        "Figure 5. Mean intervention effect trajectories and propagation timelines of Stage 3-supported paths. "
        "Panels a and c show Schelling and Deffuant, respectively, at simulation times 0-30. "
        "Representatives are taken directly from the saved representative-path selection; their saved "
        "IDs and holdout status are listed below. Curves show the saved primary-discovery mean standardised paired "
        "effect, with the saved bootstrap interval bounds as shading. Blue solid, blue dashed and red "
        "solid lines denote Micro, Meso and Macro, respectively; each response panel has a complete "
        "three-curve legend centred below it. Dotted vertical lines mark the saved onsets and every "
        "line is directly labelled; coincident scale onsets share one combined label. Text for nearby "
        "onsets is staggered across the upper plot edge while onset-line coordinates remain unchanged. "
        "Panels b and d include every path whose final primary path_classification is supported, "
        "without additional selection by onset order, significance or holdout outcome. Each path uses its "
        "saved Micro onset as time zero: x_micro = 0, x_meso = meso_onset − micro_onset, and "
        "x_macro = macro_onset − micro_onset. The blue segment runs from x_micro to x_meso and the red "
        "segment runs continuously from x_meso to x_macro. Their lengths are the Micro→Meso and Meso→Macro "
        "delays, respectively; the second delay is not used as a separate position measured from zero. "
        "Blue hollow circles mark Micro/Meso and a small red square marks Macro. Coincident onsets retain "
        "zero-length segments and overlapping markers without horizontal or vertical jitter; the smaller "
        "red square sits inside the blue circle when their onsets coincide. Absolute-onset uncertainty "
        "bounds are not reused as relative-onset or delay intervals, "
        "and no delay uncertainty is inferred or drawn. Bold path labels identify "
        "the representative shown on the left. Tol and CB abbreviate tolerance and confidence_bound; minus "
        "and plus denote the saved intervention direction. Intervals, support classifications and onset "
        "detection are not recomputed.\n\n"
        + "Supported paths: " + "; ".join(
            f"{scenario.capitalize()} n={int((data['path_records'].scenario == scenario).sum())}"
            for scenario in SCENARIOS) + ".\n\n"
        +
        "| Scenario | Short label | Saved path ID | Micro → Meso → Macro onset | Micro→Meso delay | Meso→Macro delay | Representative | Holdout confirmed |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )
    for path in data["path_records"].itertuples(index=False):
        sequence = " → ".join(f"{getattr(path, scale + '_onset_time'):g}" for scale in SCALES)
        label = path.path_label.replace("|", "/")
        delays = inter_scale_delays(data["timing"][(path.scenario, path.path_id)])
        caption += (f"| {path.scenario.capitalize()} | {label} | `{path.path_id}` | {sequence} | "
                    f"{delays[0]['delay']:g} | {delays[1]['delay']:g} | {path.representative} | {path.holdout_confirmed} |\n")
    caption += "\nThe right-panel segment start/end coordinates, Micro reference onset and unchanged adjacent delays are recorded in source_data/figure_5_plotted_delays.tsv.\n"
    caption += "\nFull frozen indicator semantic names and node IDs are recorded in source_data/figure_5_supported_path_labels.tsv.\n\nInputs:\n"
    caption += "".join(f"- `{name}`\n" for name in INPUTS)
    (output / "figure_5_caption.md").write_text(caption, encoding="utf-8")
    after = {name: sha256(run / name) for name in INPUTS}
    if before != after:
        raise RuntimeError("A source artifact changed during rendering")
    report = {"status": "passed", "source_run": str(run), "source_sha256": before,
        "input_unchanged": True, "representatives": data["representatives"],
        "saved_selection_rule": data["selection_rule"], "panels": audit,
        "supported_path_count": len(data["path_records"]), "plotted_delay_count": len(delay_records),
        "effect_points": len(data["curves"]), "experiment_recalculation": False,
        "rendering_derived_quantity": "segment start/end coordinates relative to saved Micro onset",
        "column_width_fractions": column_width_fractions, "figure_legend_count": len(fig.legends),
        "delay_uncertainty_shown": False, "alternating_row_shading": False,
        "delay_horizontal_jitter": False, "delay_vertical_jitter": False,
        "script_sha256": sha256(Path(__file__)),
        "outputs": {path.name: sha256(path) for path in exports}}
    (qa_dir / "figure_5_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path,
                        default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = render(args.run.resolve(), args.output_dir.resolve())
    print(json.dumps({"status": result["status"], "representatives": result["representatives"],
        "supported_path_count": result["supported_path_count"], "plotted_delay_count": result["plotted_delay_count"],
        "outputs": list(result["outputs"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
