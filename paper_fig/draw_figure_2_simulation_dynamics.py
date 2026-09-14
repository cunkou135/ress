"""Redraw paper Figure 2 in the original CAMO manuscript style.

Requirements: Python, numpy, pandas, matplotlib; Arial is preferred.
Run: python draw_figure_2_simulation_dynamics.py
Defaults: baoba20260904_01, baseline seed 3101, output beside this script.
Only output files are written. The input run is read without importing its code.

The layout, rcParams, colours, snapshot times, marker sizes, line styles,
axis rules, legends and export settings are copied from original figure_1().
The fixed display-jitter seed 1101 is retained solely to position opinion dots
vertically; it is unrelated to the simulation seed and carries no data value.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Patch

ORIGINAL_MODULE_SHA256 = '8b9040819ca9c744c0300cdb02876123924940082220eaf9ae1318c20ce2fe54'

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
        "font.size": 7,
        "axes.linewidth": 1.0,
        "axes.edgecolor": "#20282E",
        "axes.facecolor": "#FCFBF8",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelcolor": "#20282E",
        "xtick.color": "#20282E",
        "ytick.color": "#20282E",
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.9,
        "ytick.major.width": 0.9,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "savefig.transparent": False,
        "figure.facecolor": "#FCFBF8",
        "savefig.facecolor": "#FCFBF8",
    }
)

COLORS = {
    "blue": "#2B5D7E",
    "orange": "#C98652",
    "teal": "#2F8881",
    "purple": "#786A8F",
    "grey": "#6F777B",
    "light_grey": "#D9DAD7",
    "red": "#B84A3C",
    "micro": "#E4EEF3",
    "meso": "#E1EFEC",
    "macro": "#F3E6DC",
    "paper": "#FCFBF8",
    "ink": "#20282E",
}

def _panel_letter(ax: plt.Axes, letter: str) -> None:
    ax.text(-0.11, 1.06, letter, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top")

def _style_axes(ax: plt.Axes, *, grid: bool = False) -> None:
    """Apply the shared muted, high-contrast journal style."""
    ax.set_facecolor(COLORS["paper"])
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["bottom"].set_linewidth(1.0)
    ax.tick_params(length=3.0, width=0.9, labelsize=6.2, pad=2)
    if grid:
        ax.grid(axis="y", color="#D7D8D4", lw=0.55, alpha=0.55, zorder=0)

def _export(fig: plt.Figure, output_root: Path, stem: str, config: dict[str, Any]) -> list[str]:
    output_root.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for fmt in config["exports"]["formats"]:
        suffix = "tiff" if fmt.lower() in {"tif", "tiff"} else fmt.lower()
        path = output_root / f"{stem}.{suffix}"
        kwargs: dict[str, Any] = {"bbox_inches": "tight", "pad_inches": 0.03}
        if suffix in {"tiff", "png"}:
            kwargs["dpi"] = int(config["exports"]["tiff_dpi"] if suffix == "tiff" else 300)
        fig.savefig(path, format=suffix, **kwargs)
        written.append(str(path))
    plt.close(fig)
    return written

def render_figure_2(schelling: dict[str, np.ndarray], deffuant: dict[str, np.ndarray], output_root: Path, config: dict[str, Any]) -> list[str]:
    """Original paper Figure 2 drawing logic; only its data inputs are replaced."""
    state_grid = schelling["state_grid"]
    schelling_trace_max_time = state_grid.shape[0] - 1
    deffuant_trace_max_time = deffuant["state_opinion"].shape[0] - 1
    schelling_steps = np.array([0, 20, 60, 120], dtype=int)
    deffuant_steps = np.array([0, 40, 80, deffuant_trace_max_time], dtype=int)
    fig = plt.figure(figsize=(7.20, 5.15))
    grid = fig.add_gridspec(
        3,
        4,
        height_ratios=[1.0, 0.92, 0.72],
        hspace=0.36,
        wspace=0.13,
    )
    schelling_axes = [fig.add_subplot(grid[0, col]) for col in range(4)]
    deffuant_axes = [fig.add_subplot(grid[1, col]) for col in range(4)]
    trace_grid = grid[2, :].subgridspec(1, 2, wspace=0.32)
    trace_axes = [fig.add_subplot(trace_grid[0, 0]), fig.add_subplot(trace_grid[0, 1])]
    grid_cmap = ListedColormap(["#F7F5EF", COLORS["blue"], COLORS["red"]])
    grid_norm = BoundaryNorm([-1.5, -0.5, 0.5, 1.5], grid_cmap.N)
    opinion_cmap = LinearSegmentedColormap.from_list(
        "opinion", [COLORS["blue"], "#F7F3E5", COLORS["red"]]
    )
    rng = np.random.default_rng(1101)
    y_jitter = rng.uniform(-0.34, 0.34, deffuant["state_opinion"].shape[1])
    for col, step in enumerate(schelling_steps):
        ax = schelling_axes[col]
        ax.imshow(schelling["state_grid"][step], cmap=grid_cmap, norm=grid_norm, interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#D0D0D0")
            spine.set_linewidth(0.5)
        ax.set_title(f"t = {step}", fontsize=7, pad=2)
    for col, step in enumerate(deffuant_steps):
        ax = deffuant_axes[col]
        opinions = deffuant["state_opinion"][step]
        ax.scatter(opinions, y_jitter, c=opinions, cmap=opinion_cmap, vmin=-1, vmax=1, s=7, alpha=0.74, linewidth=0)
        ax.axvline(0.0, color="#B8B8B8", lw=0.55, ls=(0, (2, 2)))
        ax.set_xlim(-1.02, 1.02)
        ax.set_ylim(-0.42, 0.42)
        ax.set_yticks([])
        ax.set_xlabel("Opinion" if col in {1, 2} else "", labelpad=1)
        ax.set_title(f"t = {step}", fontsize=7, pad=2)
        if col:
            ax.spines["left"].set_visible(False)
    schelling_axes[0].set_ylabel("Schelling\nagent state", fontsize=7, labelpad=6)
    deffuant_axes[0].set_ylabel("Deffuant\nopinion state", fontsize=7, labelpad=6)
    _panel_letter(schelling_axes[0], "a")
    _panel_letter(deffuant_axes[0], "b")

    trace = trace_axes[0]
    changed_fraction = np.zeros(state_grid.shape[0], dtype=float)
    changed_fraction[1:] = np.mean(state_grid[1:] != state_grid[:-1], axis=(1, 2))
    unhappy_fraction = schelling["unhappy_count"] / float(schelling["agent_count"][0])
    schelling_time = np.arange(schelling_trace_max_time + 1)
    trace.plot(schelling_time, unhappy_fraction[: schelling_trace_max_time + 1], color=COLORS["red"], lw=1.75, solid_capstyle="round", label="unhappy agents")
    trace.plot(schelling_time, changed_fraction[: schelling_trace_max_time + 1], color=COLORS["blue"], lw=1.75, solid_capstyle="round", label="changed cells")
    for step in schelling_steps[1:]:
        trace.axvline(step, color="#D8D8D8", lw=0.45, ls=(0, (2, 2)), zorder=0)
    trace.set_xlim(0, schelling_trace_max_time)
    trace.set_xticks([0, 40, 80, 120])
    trace.set_ylim(0, max(0.18, 1.08 * float(np.max(np.r_[unhappy_fraction, changed_fraction]))))
    trace.set_xlabel("Simulation time")
    trace.set_ylabel("Population fraction")
    trace.legend(
        loc="upper right",
        fontsize=6.0,
        ncol=2,
        handlelength=1.8,
        columnspacing=0.9,
    )
    _panel_letter(trace, "c")
    _style_axes(trace)

    trace = trace_axes[1]
    opinions = deffuant["state_opinion"]
    opinion_dispersion = np.std(opinions, axis=1)
    extreme_fraction = deffuant["extreme_agent_count"] / float(deffuant["agent_count"][0])
    deffuant_time = np.arange(deffuant_trace_max_time + 1)
    trace.plot(deffuant_time, opinion_dispersion[: deffuant_trace_max_time + 1], color=COLORS["blue"], lw=1.75, solid_capstyle="round", label="opinion dispersion")
    trace.plot(deffuant_time, extreme_fraction[: deffuant_trace_max_time + 1], color=COLORS["red"], lw=1.75, solid_capstyle="round", label="extreme agents")
    for step in deffuant_steps[1:]:
        trace.axvline(step, color="#D8D8D8", lw=0.45, ls=(0, (2, 2)), zorder=0)
    trace.set_xlim(0, deffuant_trace_max_time)
    trace.set_xticks([0, 30, 60, 90])
    trace.set_ylim(0, 1.02)
    trace.set_xlabel("Simulation time")
    trace.set_ylabel("Population statistic")
    trace.legend(
        loc="upper left",
        fontsize=6.0,
        ncol=2,
        handlelength=1.8,
        columnspacing=0.9,
    )
    _panel_letter(trace, "d")
    _style_axes(trace)
    handles = [
        Patch(facecolor=COLORS["blue"], label="group 1"),
        Patch(facecolor=COLORS["red"], label="group 2"),
        Patch(facecolor="#F7F5EF", edgecolor="#D0D0D0", label="empty"),
    ]
    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.99, 0.995), ncol=3, fontsize=6.0)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.92, bottom=0.085)
    source_root = output_root / "source_data"
    source_root.mkdir(parents=True, exist_ok=True)
    dynamics_records = [
        {
            "scenario": "schelling",
            "time": time,
            "unhappy_agent_fraction": unhappy_fraction[time],
            "changed_cell_fraction": changed_fraction[time],
            "opinion_dispersion": np.nan,
            "extreme_agent_fraction": np.nan,
            "snapshot": time in set(schelling_steps),
        }
        for time in range(len(unhappy_fraction))
    ]
    dynamics_records.extend(
        {
            "scenario": "deffuant",
            "time": time,
            "unhappy_agent_fraction": np.nan,
            "changed_cell_fraction": np.nan,
            "opinion_dispersion": opinion_dispersion[time],
            "extreme_agent_fraction": extreme_fraction[time],
            "snapshot": time in set(deffuant_steps),
        }
        for time in range(len(opinion_dispersion))
    )
    pd.DataFrame(dynamics_records).to_csv(source_root / "figure_2_dynamics.csv", index=False)
    return _export(fig, output_root, "figure_2_simulation_dynamics", config)

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_baseline(run_root: Path, scenario: str, seed: int) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    manifest_path = run_root / "data" / "baseline_simulation_manifest.json"
    expected = None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        matches = [r for r in manifest["task_records"] if r["scenario"] == scenario
                   and r["condition"] == "baseline" and int(r["seed"]) == seed]
        if len(matches) != 1:
            raise ValueError(f"Expected one baseline record for {scenario}, seed {seed}")
        record = matches[0]
        if record.get("status") != "completed":
            raise ValueError(f"Baseline is not completed: {scenario}, seed {seed}")
        path = run_root / record["raw_path"].replace("\\", "/")
        expected = record["sha256"]
    else:
        # Optional old-run mode is used only for reproduction against the old PNG.
        path = run_root / "data" / "raw_logs" / scenario / "baseline" / f"seed_{seed}.npz"
    digest = sha256(path)
    if expected is not None and digest != expected:
        raise ValueError(f"Input hash mismatch: {path}")
    required = {"state_grid", "unhappy_count", "agent_count"} if scenario == "schelling" else {
        "state_opinion", "extreme_agent_count", "agent_count"}
    with np.load(path, allow_pickle=False) as archive:
        data = {key: archive[key].copy() for key in required}
    if any(not np.isfinite(value).all() for value in data.values()):
        raise ValueError(f"Non-finite raw data: {scenario}")
    state = data["state_grid"] if scenario == "schelling" else data["state_opinion"]
    if len(state) <= (120 if scenario == "schelling" else 80):
        raise ValueError(f"Input horizon is too short for the original snapshots: {scenario}")
    return data, {"scenario": scenario, "seed": seed, "path": str(path.resolve()),
                  "sha256": digest, "state_shape": list(state.shape)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--seed", type=int, default=3101)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--formats", nargs="+", choices=["png", "svg", "pdf", "tiff"], default=["png", "svg", "pdf", "tiff"])
    args = parser.parse_args()
    run_root, output_root = args.run.resolve(), args.output_dir.resolve()
    if output_root == run_root or run_root in output_root.parents:
        raise ValueError("Choose an output directory outside the archived input run")
    schelling, source_s = load_baseline(run_root, "schelling", args.seed)
    deffuant, source_d = load_baseline(run_root, "deffuant", args.seed)
    config = {"exports": {"formats": args.formats, "tiff_dpi": 600}}
    outputs = render_figure_2(schelling, deffuant, output_root, config)
    source_csv = output_root / "source_data" / "figure_2_dynamics.csv"
    manifest = {
        "paper_figure": 2,
        "source_run": run_root.name,
        "simulation_seed": args.seed,
        "inputs": [source_s, source_d],
        "script_sha256": sha256(Path(__file__)),
        "style": {"original_module_sha256": ORIGINAL_MODULE_SHA256,
                  "figure_size_inches": [7.2, 5.15], "font": ["Arial", "DejaVu Sans", "Liberation Sans"],
                  "font_size": 7, "background": COLORS["paper"], "blue": COLORS["blue"], "red": COLORS["red"],
                  "schelling_snapshots": [0, 20, 60, 120], "deffuant_snapshots": [0, 40, 80, len(deffuant["state_opinion"])-1],
                  "opinion_display_jitter_seed": 1101, "png_dpi": 300, "tiff_dpi": 600},
        "metric_definitions": {
            "unhappy_agent_fraction": "unhappy_count / agent_count",
            "changed_cell_fraction": "fraction of grid cells differing from the preceding saved state; first value set to 0",
            "opinion_dispersion": "numpy.std of agent opinions per time step, ddof=0",
            "extreme_agent_fraction": "archived extreme_agent_count / agent_count",
            "uncertainty": "single representative baseline trajectory; no confidence bands"},
        "outputs": {Path(path).name: sha256(Path(path)) for path in outputs},
        "source_data": {str(source_csv.relative_to(output_root)): sha256(source_csv)},
        "matplotlib_version": mpl.__version__,
    }
    (output_root / "figure_2_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run": run_root.name, "seed": args.seed, "outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()
