"""Render Figure 8 only, using the two saved robustness/scalability CSVs.

Usage: python -B draw_figure_8_robustness_efficiency.py
Dependencies: matplotlib, numpy, pandas. No experiment modules are imported.
Every repeated-condition curve uses the median and 25th--75th percentile IQR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd


STEM = "figure_8_robustness_efficiency"
SCENARIOS = ("schelling", "deffuant")
INPUTS = ("analysis/observation_robustness.csv", "analysis/causal_scalability.csv")
OBSERVATION_COLUMNS = ["scenario", "factor", "noise_level", "missing_fraction", "support_threshold",
                       "repetition", "temporal_qualification_rate", "stability", "retained_edge_count"]
SCALABILITY_COLUMNS = ["scenario", "candidate_indicator_count", "repetition", "runtime_seconds",
                       "discovered_edge_count"]
COLOURS = {"schelling": "#2B5D7E", "deffuant": "#B84A3C", "ink": "#20282E",
           "grey": "#6F777B", "paper": "#FCFBF8"}
# Panel order is a rendering contract; all conditions and values come from CSV.
PANELS = (
    ("a", 0, "observation_noise", "noise_level", "temporal_qualification_rate", "Noise", "Temporal\nqualification rate"),
    ("b", 0, "observation_noise", "noise_level", "stability", "Noise", "Stability"),
    ("c", 0, "missing_values", "missing_fraction", "temporal_qualification_rate", "Missing fraction", "Temporal\nqualification rate"),
    ("d", 0, "missing_values", "missing_fraction", "stability", "Missing fraction", "Stability"),
    ("e", 1, None, "candidate_indicator_count", "runtime_seconds", "Candidate indicator count", "Stage 2 temporal\ndiscovery runtime (s)"),
    ("f", 1, None, "candidate_indicator_count", "discovered_edge_count", "Candidate indicator count", "Discovered edge count"),
    ("g", 0, "support_threshold", "support_threshold", "retained_edge_count", "Support threshold", "Retained edge count"),
    ("h", 0, "support_threshold", "support_threshold", "stability", "Support threshold", "Stability"),
)
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 7, "axes.linewidth": 1.0, "axes.edgecolor": COLOURS["ink"],
    "axes.facecolor": COLOURS["paper"], "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": COLOURS["ink"], "xtick.color": COLOURS["ink"], "ytick.color": COLOURS["ink"],
    "xtick.direction": "out", "ytick.direction": "out", "xtick.major.width": 0.9,
    "ytick.major.width": 0.9, "legend.frameon": False, "svg.fonttype": "none", "pdf.fonttype": 42,
    "svg.hashsalt": "camo-paper-figure-8", "savefig.transparent": False,
    "figure.facecolor": COLOURS["paper"], "savefig.facecolor": COLOURS["paper"],
})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_inputs(run: Path) -> list[pd.DataFrame]:
    frames = [pd.read_csv(run / INPUTS[0], usecols=OBSERVATION_COLUMNS),
              pd.read_csv(run / INPUTS[1], usecols=SCALABILITY_COLUMNS)]
    for index, frame in enumerate(frames):
        if set(frame.scenario) != set(SCENARIOS):
            raise ValueError("Unexpected scenario set; refusing to omit a scenario")
        numeric = frame.select_dtypes(include="number")
        if np.isinf(numeric.to_numpy(float)).any():
            raise ValueError("An infinite saved value cannot be plotted")
        keys = (["scenario", "factor", "noise_level", "missing_fraction", "support_threshold", "repetition"]
                if index == 0 else ["scenario", "candidate_indicator_count", "repetition"])
        if frame[keys].isna().any().any() or frame.duplicated(keys).any():
            raise ValueError("Missing or duplicate condition/repetition identity")
        frame["source_row"] = np.arange(len(frame))
    robust, scale = frames
    expected_factors = {panel[2] for panel in PANELS if panel[2] is not None}
    if set(robust.factor) != expected_factors:
        raise ValueError("Unexpected robustness factor; refusing to silently omit records")
    for metric in ("temporal_qualification_rate", "stability"):
        values = robust[metric].dropna()
        if not values.between(0, 1).all():
            raise ValueError(f"Saved {metric} is outside its defined range")
    for frame, metric in ((robust, "retained_edge_count"), (scale, "runtime_seconds"),
                           (scale, "discovered_edge_count"), (scale, "candidate_indicator_count")):
        if frame[metric].dropna().lt(0).any():
            raise ValueError(f"Negative saved {metric}")
    return frames


def summarise(frames: list[pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    summaries, observations, conditions = [], [], {}
    for letter, source_index, factor, xcol, metric, _, _ in PANELS:
        frame = frames[source_index]
        subset = frame[frame.factor.eq(factor)].copy() if factor is not None else frame.copy()
        nuisance = [name for name in ("noise_level", "missing_fraction", "support_threshold")
                    if name != xcol and name in subset]
        fixed_settings = subset[nuisance].drop_duplicates() if nuisance else pd.DataFrame()
        if nuisance and len(fixed_settings) != 1:
            raise ValueError(f"Panel {letter} would pool different fixed settings")
        conditions[letter] = {"factor": factor, "source": INPUTS[source_index], "x_column": xcol,
                              "metric": metric, "fixed_settings": fixed_settings.to_dict("records")}
        for (scenario, x), group in subset.groupby(["scenario", xcol], sort=True):
            group = group.sort_values("repetition")
            if group.repetition.duplicated().any():
                raise ValueError(f"Panel {letter} would pool duplicate repetitions")
            values = group[metric].to_numpy(float)
            finite = values[np.isfinite(values)]
            median = float(np.median(finite)) if len(finite) else np.nan
            q25, q75 = (np.quantile(finite, [0.25, 0.75], method="linear") if len(finite) >= 2
                         else (np.nan, np.nan))
            summaries.append({"panel": letter, "source_file": INPUTS[source_index], "factor": factor,
                "scenario": scenario, "x_column": xcol, "x": x, "metric": metric,
                "n_total": len(group), "n_finite": len(finite), "n_missing": len(group) - len(finite),
                "repetitions": json.dumps(group.repetition.tolist()), "median": median,
                "q25": q25, "q75": q75, "iqr_available": len(finite) >= 2})
            for row in group.to_dict("records"):
                observations.append({"panel": letter, "source_file": INPUTS[source_index],
                    "source_row": row["source_row"], "scenario": scenario, "factor": factor,
                    "x_column": xcol, "x": x, "metric": metric, "repetition": row["repetition"],
                    "value": row[metric]})
    summary = pd.DataFrame(summaries).sort_values(["panel", "scenario", "x"], ignore_index=True)
    return summary, pd.DataFrame(observations), conditions


def metric_limits(summary: pd.DataFrame, metric: str) -> tuple[float, float]:
    # Identical metrics share an axis range across panels, with all medians/IQRs visible.
    values = summary.loc[summary.metric.eq(metric), ["median", "q25", "q75"]].to_numpy(float).ravel()
    values = values[np.isfinite(values)]
    if not len(values):
        raise ValueError(f"No defined values for {metric}")
    bounded = metric in {"temporal_qualification_rate", "stability"}
    low, high = float(values.min()), float(values.max())
    span = max(high - low, 0.02 if bounded else 1e-3)
    low, high = low - 0.10 * span, high + 0.10 * span
    if bounded:
        low, high = max(0.0, low), min(1.0, high)
    elif metric in {"runtime_seconds", "discovered_edge_count"}:
        low = 0.0
    else:
        low = max(0.0, low)
    return low, high


def render(run: Path, output: Path) -> dict:
    if output == run or run in output.parents:
        raise ValueError("Figure outputs must be outside the archived run")
    before = {name: sha256(run / name) for name in INPUTS}
    frames = load_inputs(run)
    summary, observations, conditions = summarise(frames)
    limits = {metric: metric_limits(summary, metric) for metric in summary.metric.unique()}
    fig, axes = plt.subplots(2, 4, figsize=(7.20, 2.80))
    for ax, panel in zip(axes.flat, PANELS):
        letter, _, _, xcol, metric, xlabel, ylabel = panel
        subset = summary[summary.panel.eq(letter)]
        for scenario in SCENARIOS:
            group = subset[subset.scenario.eq(scenario)].sort_values("x")
            if group.empty:
                raise ValueError(f"Missing scenario in panel {letter}")
            x, y, low, high = (group[col].to_numpy(float) for col in ("x", "median", "q25", "q75"))
            valid_band = np.isfinite(low) & np.isfinite(high)
            if valid_band.any():
                ax.fill_between(x, low, high, where=valid_band, color=COLOURS[scenario], alpha=0.10,
                    linewidth=0, zorder=1, gid=f"{letter}-{scenario}-iqr")
            line, = ax.plot(x, y, color=COLOURS[scenario], marker="o", ms=2.8, lw=1.75,
                solid_capstyle="round", zorder=3, gid=f"{letter}-{scenario}-median")
            np.testing.assert_allclose(line.get_ydata(), group["median"], equal_nan=True)
        x_values = np.sort(subset.x.unique())
        span = float(np.ptp(x_values))
        padding = 0.05 * (span if span > 0 else max(abs(float(x_values[0])), 1))
        ax.set_xlim(float(x_values[0]) - padding, float(x_values[-1]) + padding)
        # Ticks are thinned for the small panels; every observed condition is still plotted.
        tick_indices = np.unique(np.round(np.linspace(0, len(x_values) - 1, min(3, len(x_values)))).astype(int))
        ax.set_xticks(x_values[tick_indices])
        ax.set_ylim(*limits[metric])
        ax.yaxis.set_major_locator(MaxNLocator(nbins=3, min_n_ticks=3,
            integer=metric in {"discovered_edge_count", "retained_edge_count"}))
        ax.set_xlabel(xlabel, fontsize=6.0, labelpad=3)
        ax.set_ylabel(ylabel, fontsize=6.0, labelpad=3)
        ax.tick_params(length=3.0, width=0.9, labelsize=6.2, pad=2)
        ax.grid(axis="y", color="#D7D8D4", lw=0.55, alpha=0.55, zorder=0)
        ax.text(0, 1.14, letter, transform=ax.transAxes, fontsize=8.0, fontweight="bold",
                va="top", ha="left", clip_on=False, zorder=6)
    handles = [Line2D([0], [0], color=COLOURS[scenario], marker="o", markersize=3.8, lw=1.5,
                      label=scenario.capitalize()) for scenario in SCENARIOS]
    fig.legend(handles=handles, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.005),
        fontsize=6.1, columnspacing=1.4, handletextpad=0.45)
    fig.tight_layout(rect=(0, 0, 1, 0.91), pad=0.38, w_pad=0.42, h_pad=0.40)
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
    summary_path = source_dir / "figure_8_plotted_summary.tsv"
    repetitions_path = source_dir / "figure_8_plotted_repetitions.tsv"
    summary.to_csv(summary_path, sep="\t", index=False, na_rep="NA")
    observations.to_csv(repetitions_path, sep="\t", index=False, na_rep="NA")
    caption = (
        "Figure 8. Observation robustness, candidate-space scaling and support-threshold sensitivity. "
        "Schelling is blue and Deffuant is red throughout. Panels a/b show temporal qualification rate/stability "
        "against noise; c/d show the same metrics against missing fraction; e/f show Stage 2 temporal discovery "
        "runtime/discovered edge count against candidate indicator count; g/h show retained edge count/stability "
        "against support threshold. Every line is the median across the saved repetitions for its scenario, "
        "condition and metric. Shading is the 25th–75th percentile (IQR, linear quantile interpolation), showing "
        "between-repetition variability. "
        + " ".join(f"Panel {letter}: {', '.join(map(str, sorted(summary.loc[summary.panel.eq(letter), 'n_total'].unique())))} "
                    "saved repetitions per scenario/condition." for letter, *_ in PANELS)
        + " Temporal qualification rate is retained candidate relations / total candidate relations. "
        "The saved stability metric is the mean bootstrap support of retained edges within each run; "
        "the displayed median/IQR then summarises that saved metric across repeated runs. "
        "Panel e reports the saved Stage 2 temporal-discovery benchmark time in seconds, covering target-block "
        "preparation and point-estimate graph discovery. Its timing excludes bootstrap resampling, Stage 1, "
        "Stage 3 and the rest of the pipeline; it is not total workflow runtime. Panel f counts the edges "
        "discovered by that same point-estimate scalability benchmark. "
        "Panels a/b, c/d and g/h respectively use the observation_noise, missing_values and support_threshold "
        "factor rows, with all saved levels retained. Each factor keeps its own zero-perturbation observations; "
        "records from different factors are not pooled. Fixed settings are "
        + "; ".join(f"{label}: " + ", ".join(f"{key}={value:g}" for key, value in conditions[letter]["fixed_settings"][0].items())
                    for letter, label in (("a", "noise"), ("c", "missing"), ("g", "threshold")))
        + ". Identical metrics share the same y-axis range across panels. Missing values, if present, remain "
        "missing; a group without repeated defined observations receives no IQR band. "
        "No experiment, threshold, method or saved scientific result is changed.\n\n"
        "Source data: source_data/figure_8_plotted_summary.tsv and source_data/figure_8_plotted_repetitions.tsv.\n\n"
        "Inputs:\n" + "".join(f"- `{name}`\n" for name in INPUTS)
    )
    (output / "figure_8_caption.md").write_text(caption, encoding="utf-8")
    if before != {name: sha256(run / name) for name in INPUTS}:
        raise RuntimeError("A source artifact changed during rendering")
    report = {"status": "passed", "source_run": str(run), "source_sha256": before,
        "input_rows": {INPUTS[index]: len(frame) for index, frame in enumerate(frames)},
        "panel_conditions": conditions, "summary_points": len(summary), "plotted_observations": len(observations),
        "repetition_counts_by_panel": {letter: sorted(summary.loc[summary.panel.eq(letter), "n_total"].unique().tolist())
                                       for letter, *_ in PANELS},
        "centre": "median", "shading": "25th-75th percentile IQR across saved repetitions",
        "quantile_method": "linear", "missing_observations": int(observations.value.isna().sum()),
        "metric_axis_limits": limits, "scenario_colours": {key: COLOURS[key] for key in SCENARIOS},
        "runtime_scope": "Stage 2 target-block preparation plus point-estimate graph discovery",
        "axes_count": 8, "legend_count": 1, "input_unchanged": True, "experiment_recalculation": False,
        "script_sha256": sha256(Path(__file__)), "outputs": {path.name: sha256(path) for path in exports},
        "source_tables": {path.name: sha256(path) for path in (summary_path, repetitions_path)}}
    (qa_dir / "figure_8_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path,
        default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = render(args.run.resolve(), args.output_dir.resolve())
    print(json.dumps({key: result[key] for key in ("status", "summary_points", "repetition_counts_by_panel", "outputs")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
