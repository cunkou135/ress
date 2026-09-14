"""Rendering utilities used exclusively by the new Figures 9--12."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

SCENARIOS = ("schelling", "deffuant")
COLOURS = {"schelling": "#2B5D7E", "deffuant": "#B84A3C", "ink": "#20282E",
           "grey": "#6F777B", "paper": "#FCFBF8", "grid": "#D7D8D4"}

def style(number: int) -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "font.size": 7,
        "axes.linewidth": 1.0, "axes.edgecolor": COLOURS["ink"], "axes.labelcolor": COLOURS["ink"],
        "axes.facecolor": COLOURS["paper"], "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": COLOURS["ink"], "ytick.color": COLOURS["ink"],
        "xtick.major.width": .9, "ytick.major.width": .9, "legend.frameon": False,
        "svg.fonttype": "none", "pdf.fonttype": 42, "svg.hashsalt": f"camo-paper-figure-{number}",
        "savefig.transparent": False, "figure.facecolor": COLOURS["paper"],
        "savefig.facecolor": COLOURS["paper"],
    })

def axes_style(ax, letter: str, grid: str = "y") -> None:
    ax.tick_params(length=3, width=.9, labelsize=6.2, pad=2)
    if grid:
        ax.grid(axis=grid, color=COLOURS["grid"], lw=.55, alpha=.55, zorder=0)
    ax.text(0, 1.10, letter, transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")

def scenario_legend(fig, y: float = .99, *, line: bool = True) -> None:
    handles = [Line2D([0], [0], color=COLOURS[s], marker="o", markersize=4,
        lw=1.75 if line else 0, label=s.capitalize()) for s in SCENARIOS]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, y), ncol=2,
               fontsize=6.5, columnspacing=1.8, handletextpad=.5)

def arguments(description: str) -> tuple[Path, Path]:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--run", type=Path, default=Path(__file__).resolve().parents[1]/"runs"/"baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    run, output = args.run.resolve(), args.output_dir.resolve()
    if output == run or run in output.parents:
        raise ValueError("Figure outputs must be outside the archived run")
    return run, output

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def hashes(run: Path, inputs: tuple[str, ...]) -> dict:
    return {name: sha256(run/name) for name in inputs}

def unique(frame: pd.DataFrame, keys: list[str]) -> None:
    if frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise ValueError(f"Missing or duplicate identities: {keys}")

def boolean(value) -> bool:
    if str(value) not in {"True", "False"}:
        raise ValueError(f"Unexpected saved Boolean {value!r}")
    return str(value) == "True"

def finish(fig, number: int, stem: str, run: Path, output: Path, before: dict,
           tables: dict[str, pd.DataFrame], caption: str, audit: dict, script: str) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    for name in ("source_data", "qa"):
        (output/name).mkdir(exist_ok=True)
    fig.canvas.draw()
    exports = {}
    for extension in ("png", "svg"):
        path = output/f"{stem}.{extension}"
        fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=.03)
        exports[path.name] = sha256(path)
    plt.close(fig)
    table_hashes = {}
    for name, frame in tables.items():
        path = output/"source_data"/name
        frame.to_csv(path, sep="\t", index=False, na_rep="NA")
        table_hashes[name] = sha256(path)
    (output/f"figure_{number}_caption.md").write_text(caption, encoding="utf-8")
    if before != hashes(run, tuple(before)):
        raise RuntimeError("A source artifact changed during plotting")
    result = {"status": "passed", "figure": number, "source_run": str(run), "source_sha256": before,
        "source_unchanged": True, "experiment_recalculation": False, "outputs": exports,
        "source_tables": table_hashes, "script_sha256": sha256(Path(script)),
        "helper_sha256": sha256(Path(__file__)), **audit}
    (output/"qa"/f"figure_{number}_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("status", "figure", "outputs")}, ensure_ascii=False))
    return result

