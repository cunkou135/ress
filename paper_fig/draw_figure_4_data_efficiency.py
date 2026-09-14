"""Render only paper Figure 4 from the archived data-efficiency CSV.

Run: python draw_figure_4_data_efficiency.py
Dependencies: numpy, pandas, matplotlib. No experiment code is imported.
The original Figure 4 blue/red palette, circular/square markers, solid/dashed
lines, linewidths and band opacity are retained in two scenario panels.
Both methods use repeated-subsample medians and 25th-75th percentile bands.
Saved bootstrap endpoints are not read. Missing estimates remain missing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCENARIOS = ("schelling", "deffuant")
METHODS = ("full_method", "trajectory_vote")
METRICS = ("temporal_qualification_rate", "stability")
METHOD_LABELS = {"full_method": "Full method", "trajectory_vote": "Trajectory vote"}
METRIC_LABELS = {"temporal_qualification_rate": "Temporal qualification rate", "stability": "Stability"}
COLORS = {"full_method": "#2B5D7E", "trajectory_vote": "#B84A3C",
          "ink": "#20282E", "grey": "#6F777B"}
STEM = "figure_4_data_efficiency"
CSV_RELATIVE = "analysis/data_efficiency_repeated_subsampling.csv"
REQUIRED_COLUMNS = ["scenario", "method", "trajectory_count", "repetition",
                    "temporal_qualification_rate", "stability", "stability_estimable"]
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 7, "axes.linewidth": 1.0,
    "axes.edgecolor": COLORS["ink"], "axes.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": COLORS["ink"], "xtick.color": COLORS["ink"],
    "ytick.color": COLORS["ink"], "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.width": 0.9, "ytick.major.width": 0.9,
    "legend.frameon": False, "svg.fonttype": "none", "pdf.fonttype": 42,
    "svg.hashsalt": "camo-paper-figure-4", "savefig.transparent": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv(path: Path) -> pd.DataFrame:
    # Select only identifiers, saved point estimates and the estimability flag.
    # In particular, bootstrap interval columns cannot enter this figure.
    data = pd.read_csv(path, usecols=REQUIRED_COLUMNS)
    if set(data["scenario"]) != set(SCENARIOS) or set(data["method"]) != set(METHODS):
        raise ValueError("Unexpected scenario or method set; refusing to silently omit rows")
    keys = ["scenario", "method", "trajectory_count", "repetition"]
    if data[keys].isna().any().any() or data.duplicated(keys).any():
        raise ValueError("Missing or duplicate repeated-subsample keys")
    counts = data["trajectory_count"].to_numpy(dtype=float)
    if not np.isfinite(counts).all() or not ((counts > 0) & (counts == np.floor(counts))).all():
        raise ValueError("Invalid number of trajectories")
    for metric in METRICS:
        data[metric] = pd.to_numeric(data[metric], errors="raise")
        values = data[metric].dropna().to_numpy(dtype=float)
        if not np.isfinite(values).all() or np.any((values < 0) | (values > 1)):
            raise ValueError(f"Invalid probability-scale values in {metric}")
    estimable = data["stability_estimable"].astype(str)
    if not estimable.isin(["True", "False"]).all():
        raise ValueError("Unexpected stability_estimable values")
    if data.loc[estimable == "False", "stability"].notna().any():
        raise ValueError("CSV contains a stability estimate flagged as non-estimable")
    return data


def summarise(data: pd.DataFrame) -> pd.DataFrame:
    """Describe saved repeated-subsample values with median and IQR.

    Quartiles use linear interpolation between ordered finite observations.
    Entirely missing groups remain NA in the line and both band boundaries.
    These descriptive bands are not confidence intervals.
    """
    rows = []
    for scenario in SCENARIOS:
        for method in METHODS:
            selected = data[(data.scenario == scenario) & (data.method == method)]
            for metric in METRICS:
                for count, group in selected.groupby("trajectory_count", sort=True):
                    point = group[metric].dropna()
                    rows.append({
                        "scenario": scenario, "method": method, "metric": metric,
                        "trajectory_count": int(count), "repeated_subsamples": len(group),
                        "median": float(point.median()) if len(point) else np.nan,
                        "q25": float(point.quantile(0.25, interpolation="linear")) if len(point) else np.nan,
                        "q75": float(point.quantile(0.75, interpolation="linear")) if len(point) else np.nan,
                        "finite_point_count": len(point),
                    })
    return pd.DataFrame(rows)


def style_axes(ax) -> None:
    ax.set_facecolor("white")
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["bottom"].set_linewidth(1.0)
    ax.tick_params(length=3.0, width=0.9, labelsize=6.2, pad=2)
    ax.grid(axis="y", color="#D7D8D4", lw=0.55, alpha=0.55, zorder=0)


def render(run: Path, output: Path) -> dict:
    if output == run or run in output.parents:
        raise ValueError("Figure output must be outside the archived run")
    source = run / CSV_RELATIVE
    before_hash = sha256(source)
    raw = load_csv(source)
    summary = summarise(raw)
    trajectory_counts = np.sort(raw.trajectory_count.unique())
    fig, axes = plt.subplots(1, 2, figsize=(7.20, 3.15), sharex=True, sharey=False)
    fig.subplots_adjust(left=0.075, right=0.98, bottom=0.16, top=0.89,
                        wspace=0.24)
    audit = {}
    for col, scenario in enumerate(SCENARIOS):
        ax = axes[col]
        letter = chr(ord("a") + col)
        panel = {}
        for method in METHODS:
            panel[method] = {}
            for metric in METRICS:
                values = summary[(summary.scenario == scenario) & (summary.method == method)
                                 & (summary.metric == metric)].sort_values("trajectory_count")
                x = values.trajectory_count.to_numpy(dtype=float)
                y = values["median"].to_numpy(dtype=float)
                low = values.q25.to_numpy(dtype=float)
                high = values.q75.to_numpy(dtype=float)
                qualification = metric == "temporal_qualification_rate"
                line, = ax.plot(x, y, marker="o" if qualification else "s", ms=3.7, lw=1.9,
                    ls="solid" if qualification else (0, (3, 2)), color=COLORS[method],
                    solid_capstyle="round", label=f"{METHOD_LABELS[method]} | {METRIC_LABELS[metric]}",
                    gid=f"{letter}-{method}-{metric}-line")
                valid_band = np.isfinite(low) & np.isfinite(high)
                # Preserve NA at its actual x location in both line and band.
                # In particular, do not filter x/y and bridge across missing data.
                if valid_band.any():
                    ax.fill_between(x, low, high, where=valid_band,
                        color=COLORS[method], alpha=0.085, linewidth=0,
                        interpolate=False, gid=f"{letter}-{method}-{metric}-iqr")
                stored_y = np.asarray(line.get_ydata(), dtype=float)
                np.testing.assert_allclose(stored_y, y, equal_nan=True)
                panel[method][metric] = {
                    "point_counts": x[np.isfinite(y)].astype(int).tolist(),
                    "na_point_counts": x[~np.isfinite(y)].astype(int).tolist(),
                    "iqr_counts": x[valid_band].astype(int).tolist(),
                    "na_iqr_counts": x[~valid_band].astype(int).tolist(),
                }
        ax.set_xticks(trajectory_counts)
        ax.set_xlim(float(trajectory_counts.min())-0.7, float(trajectory_counts.max())+0.8)
        y_min = 0.5 if scenario == "schelling" else 0.0
        ax.set_ylim(y_min, 1)
        ax.set_yticks(np.linspace(y_min, 1, 6))
        ax.set_xlabel("Number of trajectories")
        ax.set_ylabel("Score")
        ax.set_title(scenario.capitalize(), fontsize=8, pad=6)
        ax.tick_params(axis="x", labelbottom=True)
        ax.tick_params(axis="y", labelleft=True)
        style_axes(ax)
        ax.text(-0.12, 1.08, letter, transform=ax.transAxes,
                fontsize=9, fontweight="bold", va="top")
        ax.legend(loc="lower left", fontsize=6.0, handlelength=2.6,
                  borderaxespad=0.6, labelspacing=0.45)
        audit[letter] = {"scenario": scenario, "y_limits": list(ax.get_ylim()), "methods": panel}
    fig.canvas.draw()
    output.mkdir(parents=True, exist_ok=True)
    outputs = []
    for extension in ("svg", "png"):
        path = output / f"{STEM}.{extension}"
        fig.savefig(path, format=extension, dpi=300, bbox_inches="tight", pad_inches=0.03)
        outputs.append(path)
    plt.close(fig)
    source_dir, qa_dir = output / "source_data", output / "qa"
    source_dir.mkdir(exist_ok=True)
    qa_dir.mkdir(exist_ok=True)
    summary_path = source_dir / "figure_4_plotted_summary.tsv"
    summary.to_csv(summary_path, sep="\t", index=False, na_rep="NA")
    counts = sorted(raw.groupby(["scenario", "method", "trajectory_count"]).size().unique().tolist())
    repetition_text = str(counts[0]) if len(counts) == 1 else ", ".join(map(str, counts))
    caption = (
        "Figure 4. Temporal qualification rate and stability with increasing trajectory availability. "
        "Panel a shows Schelling on a 0.5-1 vertical scale; panel b shows Deffuant on a 0-1 vertical scale. "
        "Blue denotes Full method and red denotes Trajectory vote. Solid lines with circular markers "
        "show temporal qualification rate, defined as retained candidate relations divided by total "
        "candidate relations; dashed lines with square markers show the saved stability statistic. "
        f"For each scenario, method, trajectory count and metric, the centre line is the median of the "
        f"{repetition_text} saved repeated subsamples and the shaded band spans their 25th-75th percentiles "
        "(IQR; linear interpolation between ordered observations), using the same aggregation for both methods. "
        "Shading represents repeated-subsample variability, not a confidence interval. Saved bootstrap "
        "interval columns are not used and no new subsampling is performed. Missing stability at one "
        "trajectory remains absent for both methods, without zero filling or connecting across missing values.\n\n"
        "The exact plotted medians, quartiles, and nonmissing counts are provided in "
        "source_data/figure_4_plotted_summary.tsv. This figure reads only " + CSV_RELATIVE + ".\n"
    )
    (output / "figure_4_caption.md").write_text(caption, encoding="utf-8")
    after_hash = sha256(source)
    if before_hash != after_hash:
        raise RuntimeError("Source CSV changed during rendering")
    report = {
        "status": "passed", "source_run": run.name, "source_csv": str(source),
        "input_sha256": before_hash, "input_rows": len(raw), "columns_used": REQUIRED_COLUMNS,
        "trajectory_counts": trajectory_counts.tolist(), "repeated_subsample_counts": counts,
        "aggregation": "median and 25th-75th percentiles of finite repeated-subsample values; entirely missing groups remain NA",
        "quantile_interpolation": "linear", "band_meaning": "repeated-subsample variability (IQR), not a confidence interval",
        "bootstrap_ci_columns_used": False, "new_resampling": False,
        "interval_imputation": False, "point_imputation": False,
        "panels": audit, "script_sha256": sha256(Path(__file__)),
        "outputs": {path.name: sha256(path) for path in outputs},
        "plotted_summary_sha256": sha256(summary_path), "input_unchanged": before_hash == after_hash,
        "matplotlib_version": mpl.__version__,
    }
    (qa_dir / "figure_4_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path,
        default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = render(args.run.resolve(), args.output_dir.resolve())
    print(json.dumps({"status": result["status"], "panels": result["panels"],
                      "outputs": list(result["outputs"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
