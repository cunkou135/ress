"""Render paper Figure 3: frozen candidate paths and their saved stage filters.

Run with: python draw_figure_3_graph_recovery.py
Dependencies: matplotlib, numpy. No experiment module is imported or executed.
The legacy figure_3_graph_recovery stem is retained for compatibility.
All scientific membership and counts come from five archived run files.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import textwrap

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


SCENARIOS = ("schelling", "deffuant")
SCALES = ("parameter", "micro", "meso", "macro")
STEM = "figure_3_graph_recovery"
INPUTS = (
    "representation/indicators_frozen.json",
    "representation/candidate_paths.json",
    "analysis/path_temporal_qualification.csv",
    "analysis/path_intervention_classification.csv",
    "analysis/holdout_path_confirmation.csv",
)
TITLES = (
    "Stage 1 | LLM candidate paths",
    "Stage 2 | Temporal qualification",
    "Stage 3 | Intervention support",
)
# Original CAMO node shape, scale fills, blue and outline colours. The white
# page and light-grey panels follow the requested Figure 3 presentation.
COLORS = {
    "ink": "#20282E", "outline": "#465057", "grey": "#6F777B",
    "panel": "#F3F2ED", "panel_border": "#E2E1DC",
    "parameter": "#ECECE8", "micro": "#E4EEF3",
    "meso": "#E1EFEC", "macro": "#F3E6DC",
    "stage1": "#A8BBC8", "stage2": "#527F9D", "stage3": "#2B5D7E",
}
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 7, "axes.linewidth": 1.0,
    "axes.edgecolor": COLORS["ink"], "axes.labelcolor": COLORS["ink"],
    "text.color": COLORS["ink"], "legend.frameon": False,
    "svg.fonttype": "none", "svg.hashsalt": "camo-paper-figure-3",
    "pdf.fonttype": 42, "figure.facecolor": "white",
    "savefig.facecolor": "white", "savefig.transparent": False,
})


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def saved_boolean(value: str) -> bool:
    """Parse saved booleans; never apply Python truthiness to CSV strings."""
    if value not in {"True", "False"}:
        raise ValueError(f"Unexpected archived Boolean: {value!r}")
    return value == "True"


def read_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def index_rows(rows: list[dict], scenario: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        if row["scenario"] != scenario:
            continue
        key = row["path_id"]
        if key in result:
            raise ValueError(f"Duplicate saved path row: {scenario}:{key}")
        result[key] = row
    return result


def chain(path: dict) -> tuple[str, str, str, str]:
    return ("parameter:" + path["parameter"], path["micro_indicator"],
            path["meso_indicator"], path["macro_indicator"])


def project(paths: list[dict], stage: int) -> dict[tuple[str, str], list[str]]:
    """Union of saved complete paths; Stage 2 omits parameter connectors."""
    membership = {}
    for path in paths:
        nodes = chain(path)
        for i in ((1, 2) if stage == 2 else (0, 1, 2)):
            membership.setdefault((nodes[i], nodes[i + 1]), []).append(path["path_id"])
    return {edge: sorted(ids) for edge, ids in sorted(membership.items())}


def load_evidence(run: Path) -> dict:
    frozen = json.loads((run / INPUTS[0]).read_text(encoding="utf-8"))
    candidates = json.loads((run / INPUTS[1]).read_text(encoding="utf-8"))
    temporal = read_rows(run / INPUTS[2])
    intervention = read_rows(run / INPUTS[3])
    holdout = read_rows(run / INPUTS[4])
    evidence = {}
    for scenario in SCENARIOS:
        indicators = frozen["scenarios"][scenario]["indicators"]
        paths = candidates["scenarios"][scenario]
        by_id = {node["id"]: node for node in indicators}
        by_path = {path["path_id"]: path for path in paths}
        if len(by_id) != len(indicators) or len(by_path) != len(paths):
            raise ValueError(f"Duplicate frozen ID: {scenario}")
        t, i, h = (index_rows(rows, scenario) for rows in (temporal, intervention, holdout))
        if set(t) != set(by_path) or set(i) != set(by_path):
            raise ValueError(f"Stage tables do not cover the frozen path set: {scenario}")
        if not set(h).issubset(by_path):
            raise ValueError(f"Unknown holdout path: {scenario}")
        for path in paths:
            pid = path["path_id"]
            for scale in ("micro", "meso", "macro"):
                nid = path[f"{scale}_indicator"]
                if nid not in by_id or by_id[nid]["scale"] != scale:
                    raise ValueError(f"Frozen indicator/scale mismatch: {pid}:{nid}")
                for row in (t[pid], i[pid], *([h[pid]] if pid in h else [])):
                    if row[scale] != nid or row["parameter"] != path["parameter"]:
                        raise ValueError(f"Saved path definition mismatch: {scenario}:{pid}")
            if i[pid]["direction"] != path["intervention_direction"]:
                raise ValueError(f"Saved intervention direction mismatch: {pid}")
            if pid in h and h[pid]["direction"] != path["intervention_direction"]:
                raise ValueError(f"Saved holdout direction mismatch: {pid}")
        qualified = {pid for pid, row in t.items() if saved_boolean(row["path_temporally_qualified"])}
        supported = {pid for pid, row in i.items() if row["path_classification"] == "supported"}
        confirmed = {pid for pid, row in h.items() if row["classification"] == "confirmed"}
        for pid, row in h.items():
            if saved_boolean(row["holdout_confirmed"]) != (pid in confirmed):
                raise ValueError(f"Inconsistent archived holdout flags: {pid}")
        if not confirmed.issubset(supported) or not supported.issubset(qualified):
            raise ValueError(f"Saved stage sets are not nested: {scenario}")
        # Filtering uses only the two requested stored predicates. Holdout does
        # not add or remove any Stage 3 path.
        stage_paths = {
            1: list(paths),
            2: [p for p in paths if p["path_id"] in qualified],
            3: [p for p in paths if p["path_id"] in supported],
        }
        evidence[scenario] = {
            "indicators": indicators, "paths": paths, "temporal": t,
            "intervention": i, "holdout": h, "confirmed": confirmed,
            "stage_paths": stage_paths,
            "stage_edges": {stage: project(selected, stage) for stage, selected in stage_paths.items()},
        }
    return evidence


def semantic_label(node: dict) -> str:
    """Display-only abbreviations, applied to semantic_name, never to evidence."""
    text = node.get("semantic_name") or node["id"].replace("_", " ")
    substitutions = (
        (r"standard deviation", "SD"), (r"25th percentile", "P25"),
        (r"75th percentile", "P75"), (r"Between-district", "District"),
        (r"neighborhood", "nbr."), (r"Whole-system", "Global"),
        (r"Fraction of unsatisfied agents", "Unsatisfied fraction"),
        (r"Fraction of agents relocating", "Relocating fraction"),
        (r"among unsatisfied agents", "(unsatisfied)"),
        (r"among movers", "(movers)"), (r"same-group", "same-grp."),
        (r"group-composition", "group"), (r"boundary-agent", "boundary"),
        (r"interaction", "interact."), (r"destination", "dest."),
        (r"similarity", "sim."), (r"relocation", "reloc."),
        (r"neighbour", "nbr."), (r"fraction", "frac."),
        (r"variance", "var."), (r"absolute", "abs."),
        (r"distribution", "distr."), (r"sampled ", ""),
        (r"\bof\b", ""),
    )
    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text[0].upper() + text[1:]


def fixed_layout(item: dict) -> dict[str, dict]:
    """Compute once from frozen file order, and reuse verbatim in all columns."""
    parameters = list(dict.fromkeys(p["parameter"] for p in item["paths"]))
    groups = {"parameter": [{"id": "parameter:" + p, "scale": "parameter",
                              "semantic_name": p.replace("_", " ")} for p in parameters]}
    groups.update({scale: [n for n in item["indicators"] if n["scale"] == scale]
                   for scale in ("micro", "meso", "macro")})
    centers = {"parameter": 0.52, "micro": 1.77, "meso": 3.08, "macro": 4.42}
    widths = {"parameter": 0.92, "micro": 1.04, "meso": 1.15, "macro": 1.10}
    layout = {}
    for scale in SCALES:
        group = groups[scale]
        ys = np.linspace(0.902, 0.100, len(group)) if len(group) > 1 else [0.501]
        for rank, (node, y) in enumerate(zip(group, ys)):
            label = (node["semantic_name"].capitalize() if scale == "parameter" else semantic_label(node))
            wrapped = textwrap.fill(label, width=23 if scale in {"micro", "meso"} else 21,
                                    break_long_words=False, break_on_hyphens=False)
            # Wider-spaced meso/macro groups can accommodate three-line names.
            line_count = wrapped.count("\n") + 1
            height = max(0.042, 0.020 * line_count + 0.006)
            layout[node["id"]] = {
                "x": centers[scale], "y": float(y), "width": widths[scale],
                "height": height, "scale": scale, "order": rank,
                "semantic_name": node["semantic_name"], "label": wrapped,
            }
    return layout


def draw_panel(ax, item: dict, layout: dict, stage: int, letter: str) -> dict:
    ax.set(xlim=(0, 5.05), ylim=(0, 1.035))
    ax.set_axis_off()
    ax.add_patch(FancyBboxPatch((0.0, 0.035), 5.04, 0.983,
                 boxstyle="round,pad=0,rounding_size=0.036",
                 facecolor=COLORS["panel"], edgecolor=COLORS["panel_border"],
                 linewidth=0.45, alpha=0.72, zorder=-5))
    for scale in SCALES:
        nodes = [v for v in layout.values() if v["scale"] == scale]
        ax.text(nodes[0]["x"], 0.993, scale.capitalize(), color=COLORS["grey"],
                ha="center", va="top", fontsize=6.5)
    edges = item["stage_edges"][stage]
    active = {node for edge in edges for node in edge}
    patches, texts = {}, []
    for nid, node in layout.items():
        x, y, w, h = (node[k] for k in ("x", "y", "width", "height"))
        is_active = nid in active
        patch = FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle="round,pad=0.001,rounding_size=0.015",
            facecolor=COLORS[node["scale"]] if is_active else "#F7F7F4",
            edgecolor=COLORS["outline"] if is_active else "#B6BEC1",
            linewidth=0.75 if is_active else 0.50, zorder=3)
        patch.set_gid(f"{letter}-node-{nid}")
        ax.add_patch(patch)
        patches[nid] = patch
        label = ax.text(x, y, node["label"], ha="center", va="center",
                       fontsize=6.0, linespacing=1.05,
                       color=COLORS["ink"] if is_active else "#818A8F", zorder=4)
        label.set_gid(f"{letter}-label-{nid}")
        texts.append((nid, label, patch))
    terminal_confirmed = {}
    if stage == 3:
        for path in item["stage_paths"][3]:
            if path["path_id"] in item["confirmed"]:
                terminal_confirmed.setdefault((path["meso_indicator"], path["macro_indicator"]), []).append(path["path_id"])
    for (source, target), members in edges.items():
        a, b = layout[source], layout[target]
        start = (a["x"] + a["width"]/2 + 0.012, a["y"])
        end = (b["x"] - b["width"]/2 - 0.016, b["y"])
        width = 0.68 + 0.14 * np.log2(len(members))
        arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=5.5,
                               linewidth=width, color=COLORS[f"stage{stage}"],
                               alpha=0.94, shrinkA=0, shrinkB=0,
                               connectionstyle="arc3,rad=0", zorder=1.9)
        arrow.set_gid(f"{letter}-edge-{source}-to-{target}")
        ax.add_patch(arrow)
        if (source, target) in terminal_confirmed:
            fraction = 0.69
            ax.plot(start[0] + fraction*(end[0]-start[0]), start[1] + fraction*(end[1]-start[1]),
                    "o", color=COLORS["ink"], markersize=2.4, markeredgewidth=0,
                    zorder=5, gid=f"{letter}-holdout-{source}-to-{target}")
    ax.text(0.01, 1.050, letter, fontsize=9, fontweight="bold", ha="left", va="bottom")
    count_text = f"{len(item['stage_paths'][stage])} paths  |  {len(edges)} unique edges"
    if stage == 3:
        count_text += f"  |  {len(item['confirmed'])} holdout confirmed"
    ax.text(2.52, 0.003, count_text, ha="center", va="bottom", fontsize=7.0)
    return {"node_artists": texts, "edge_count": len(edges),
            "node_count": len(patches), "holdout_markers": len(terminal_confirmed)}


def save_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def render(run: Path, output: Path) -> dict:
    if output == run or run in output.parents:
        raise ValueError("Figure outputs must stay outside the formal run")
    hashes = {name: digest(run / name) for name in INPUTS}
    data = load_evidence(run)
    # Each layout is constructed exactly once before the six-panel loop.
    layouts = {scenario: fixed_layout(item) for scenario, item in data.items()}
    fig, axes = plt.subplots(2, 3, figsize=(15.6, 10.3))
    fig.subplots_adjust(left=0.035, right=0.993, top=0.952, bottom=0.072,
                        wspace=0.058, hspace=0.155)
    panel_records = {}
    for row, scenario in enumerate(SCENARIOS):
        for col, stage in enumerate((1, 2, 3)):
            letter = chr(ord("a") + row*3 + col)
            ax = axes[row, col]
            if row == 0:
                ax.set_title(TITLES[col], fontsize=8.2, pad=21)
            panel_records[letter] = draw_panel(ax, data[scenario], layouts[scenario], stage, letter)
            if col == 0:
                ax.text(-0.145, 0.52, scenario.capitalize(), rotation=90,
                        ha="center", va="center", fontsize=9, fontweight="bold")
    legend = [Line2D([0], [0], color=COLORS[f"stage{s}"], linewidth=1.2,
                     label=label) for s, label in ((1, "Candidate"), (2, "Temporally qualified"), (3, "Intervention supported"))]
    legend.append(Line2D([0], [0], linestyle="none", marker="o", color=COLORS["ink"],
                         markersize=3, label="Holdout confirmed (terminal segment)"))
    fig.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.51, 0.026),
               ncol=4, fontsize=7, handlelength=2.0, columnspacing=2.2)
    fig.text(0.51, 0.012,
             "Fixed frozen-node positions across stages. Line width indicates path reuse; pale nodes remain visible without retained connections.",
             ha="center", va="center", fontsize=6.4, color=COLORS["grey"])
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    overflow = []
    for letter, record in panel_records.items():
        for nid, label, patch in record["node_artists"]:
            text_box, node_box = label.get_window_extent(renderer), patch.get_window_extent(renderer)
            if text_box.width > node_box.width-2 or text_box.height > node_box.height-1:
                overflow.append({"panel": letter, "node": nid, "label": label.get_text(),
                                 "text_pixels": [text_box.width, text_box.height],
                                 "node_pixels": [node_box.width, node_box.height]})
    if overflow:
        plt.close(fig)
        raise ValueError("Node labels overflow: " + json.dumps(overflow, ensure_ascii=False))
    output.mkdir(parents=True, exist_ok=True)
    outputs = []
    for extension in ("svg", "png"):
        path = output / f"{STEM}.{extension}"
        fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.05)
        outputs.append(path)
    plt.close(fig)
    source_dir, qa_dir = output / "source_data", output / "qa"
    source_dir.mkdir(exist_ok=True)
    qa_dir.mkdir(exist_ok=True)
    node_rows, path_rows, edge_rows, counts = [], [], [], {}
    for scenario, item in data.items():
        for nid, node in layouts[scenario].items():
            node_rows.append({"scenario": scenario, "node_id": nid, **node})
        for path in item["paths"]:
            pid = path["path_id"]
            path_rows.append({"scenario": scenario, "path_id": pid, "parameter": path["parameter"],
                "direction": path["intervention_direction"], "micro": path["micro_indicator"],
                "meso": path["meso_indicator"], "macro": path["macro_indicator"],
                "stage_1": True, "stage_2": saved_boolean(item["temporal"][pid]["path_temporally_qualified"]),
                "stage_3": item["intervention"][pid]["path_classification"] == "supported",
                "saved_primary_class": item["intervention"][pid]["path_classification"],
                "holdout_confirmed": pid in item["confirmed"]})
        counts[scenario] = {}
        for stage, selected in item["stage_paths"].items():
            edges = item["stage_edges"][stage]
            counts[scenario][str(stage)] = {"paths": len(selected), "unique_edges": len(edges),
                "nodes": len(layouts[scenario]), "holdout_confirmed": len(item["confirmed"]) if stage == 3 else None}
            for (a, b), ids in edges.items():
                edge_rows.append({"scenario": scenario, "stage": stage, "source": a, "target": b,
                    "path_reuse_count": len(ids), "path_ids": json.dumps(ids),
                    "holdout_path_ids": json.dumps([pid for pid in ids if stage == 3 and pid in item["confirmed"]]),
                    "terminal_holdout_marker": stage == 3 and layouts[scenario][a]["scale"] == "meso"
                        and any(pid in item["confirmed"] for pid in ids)})
    save_tsv(source_dir / "figure_3_node_labels_and_positions.tsv", node_rows)
    save_tsv(source_dir / "figure_3_path_membership.tsv", path_rows)
    save_tsv(source_dir / "figure_3_projected_edges.tsv", edge_rows)
    caption = (
        "Figure 3. Progressive qualification of frozen multiscale candidate paths. "
        "Rows show Schelling and Deffuant. Stage 1 projects all saved LLM candidate paths into "
        "Parameter to Micro to Meso to Macro relations. Stage 2 retains only complete paths "
        "with saved path_temporally_qualified=True, and displays their two adjacent-scale relations; "
        "parameter nodes remain in place without connectors. Stage 3 projects only complete paths "
        "with saved path_classification=supported. Every frozen indicator remains visible in every column; "
        "node order and coordinates are fixed within each scenario. Duplicate directed edges are drawn once, "
        "with width 0.68 + 0.14 log2(k) pt for k contributing paths. Dark dots mark terminal segments used by "
        "at least one primary-supported path whose saved holdout classification is confirmed. This auxiliary "
        "mark never changes primary support. Edge projection can share nodes and segments between paths; "
        "only the complete combinations listed in figure_3_path_membership.tsv are candidate or supported paths. "
        "Parameter nodes pool intervention directions; path membership retains the original minus/plus conditions.\n\n"
        "Labels are shortened from semantic_name. SD: standard deviation; P25/P75: 25th/75th percentile; "
        "nbr.: neighbour/neighborhood; sim.: similarity; frac.: fraction; var.: variance; abs.: absolute; "
        "dest.: destination; reloc.: relocation; same-grp.: same-group; interact.: interaction; distr.: distribution. "
        "The full semantic names, IDs and fixed positions are in source_data/figure_3_node_labels_and_positions.tsv.\n"
    )
    (output / "figure_3_caption.md").write_text(caption, encoding="utf-8")
    after = {name: digest(run / name) for name in INPUTS}
    if after != hashes:
        raise RuntimeError("Archived figure inputs changed during rendering")
    report = {"status": "passed", "source_run": run.name, "input_sha256": hashes,
        "script_sha256": digest(Path(__file__)), "counts": counts,
        "stage_predicates": {"1": "all candidate_paths", "2": "path_temporally_qualified == True",
                             "3": 'path_classification == "supported"'},
        "holdout_predicate": 'classification == "confirmed", cross-checked against holdout_confirmed',
        "fixed_layout": "frozen indicator file order; candidate parameter first occurrence; computed once per scenario",
        "label_overflow": overflow, "outputs": {p.name: digest(p) for p in outputs},
        "protected_inputs_unchanged": hashes == after,
        "runtime": {"matplotlib": mpl.__version__, "numpy": np.__version__}}
    (qa_dir / "figure_3_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path,
        default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = render(args.run.resolve(), args.output_dir.resolve())
    print(json.dumps({"status": result["status"], "counts": result["counts"],
                      "outputs": list(result["outputs"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
