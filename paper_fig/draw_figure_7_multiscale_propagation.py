"""Render Figure 7 from saved Stage 2/3 evidence, without running experiments.

Usage: python -B draw_figure_7_multiscale_propagation.py
Dependencies: matplotlib, numpy, pandas.
All temporal-qualified paths are shown in scenario/path_id order. Display
categories are separate from the unchanged saved scientific classifications.
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
import pandas as pd


SCENARIOS = ("schelling", "deffuant")
SCALES = ("micro", "meso", "macro")
STEM = "figure_7_multiscale_propagation"
INPUTS = (
    "analysis/path_temporal_qualification.csv",
    "analysis/path_intervention_classification.csv",
    "analysis/intervention_classifications.csv",
    "analysis/holdout_path_confirmation.csv",
    "representation/candidate_paths.json",
    "representation/indicators_frozen.json",
)
COLOURS = {"blue": "#2B5D7E", "red": "#B84A3C", "grey": "#6F777B",
           "light_grey": "#D9DAD7", "paper": "#FCFBF8", "ink": "#20282E"}
# The original Figure 7 state palette and segment widths are retained.
STATE_STYLES = {
    "supported": (COLOURS["blue"], "solid"),
    "contradicted": (COLOURS["red"], (0, (5, 2))),
    "inconclusive": (COLOURS["grey"], (0, (2, 2))),
    "manipulation_failure": (COLOURS["light_grey"], (0, (1, 2))),
}
# Presentation grouping only; raw classifications are exported alongside it.
DISPLAY_STATES = {**{state: state for state in STATE_STYLES},
                  "no_stable_downstream_effect": "inconclusive"}
STATE_LABELS = {"supported": "Supported", "contradicted": "Contradicted",
                "inconclusive": "Inconclusive", "manipulation_failure": "Manip. failure"}
PARAMETER_LABELS = {"destination_preference": "Dest", "move_probability": "Move",
    "tolerance": "Tol", "assimilation_strength": "AS", "backfire_threshold": "BT",
    "confidence_bound": "CB"}
SCOPE_LABELS = {"direct_root": "Direct root", "upstream_mediated": "Upstream mediated"}
SCOPE_MARKERS = {"direct_root": "s", "upstream_mediated": "D"}
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 7, "axes.linewidth": 1.0, "axes.edgecolor": COLOURS["ink"],
    "axes.facecolor": COLOURS["paper"], "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": COLOURS["ink"], "xtick.color": COLOURS["ink"], "ytick.color": COLOURS["ink"],
    "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.width": 0.9, "ytick.major.width": 0.9, "legend.frameon": False,
    "svg.fonttype": "none", "pdf.fonttype": 42, "svg.hashsalt": "camo-paper-figure-7",
    "savefig.transparent": False, "figure.facecolor": COLOURS["paper"],
    "savefig.facecolor": COLOURS["paper"],
})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def saved_bool(value: object) -> bool:
    if str(value) not in {"True", "False"}:
        raise ValueError(f"Missing or unexpected saved Boolean: {value!r}")
    return str(value) == "True"


def unique_keys(frame: pd.DataFrame, keys: list[str], label: str) -> None:
    if frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise ValueError(f"Missing or duplicate {label} keys")


def load_evidence(run: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    temporal, paths, attempts, holdout = [pd.read_csv(run / name) for name in INPUTS[:4]]
    candidates = json.loads((run / INPUTS[4]).read_text(encoding="utf-8"))
    indicators = json.loads((run / INPUTS[5]).read_text(encoding="utf-8"))
    keys = ["scenario", "path_id"]
    for label, frame in (("temporal", temporal), ("path classification", paths), ("holdout", holdout)):
        unique_keys(frame, keys, label)
    if set(temporal.scenario) != set(SCENARIOS):
        raise ValueError("Unexpected scenario set; refusing to omit a scenario")
    temporal["path_temporally_qualified"] = temporal.path_temporally_qualified.map(saved_bool)
    paths["path_temporally_qualified"] = paths.path_temporally_qualified.map(saved_bool)
    stage2 = temporal[temporal.path_temporally_qualified].copy()
    selected = stage2[keys].merge(paths, on=keys, how="left", validate="one_to_one", indicator=True)
    if not selected._merge.eq("both").all() or not selected.path_temporally_qualified.eq(True).all():
        raise ValueError("Stage 2 and saved path classification do not match")
    selected = selected.drop(columns="_merge")
    temporal_lookup = stage2.set_index(keys)
    holdout_lookup = holdout.set_index(keys)
    if not holdout.evaluation_track.eq("holdout_confirmation").all():
        raise ValueError("Unexpected holdout evaluation track")
    frozen_paths = {(scenario, path["path_id"]): path for scenario, records in candidates["scenarios"].items()
                    for path in records}
    if len(frozen_paths) != sum(map(len, candidates["scenarios"].values())):
        raise ValueError("Duplicate frozen candidate path")
    frozen_nodes = {(scenario, node["id"]): node for scenario, value in indicators["scenarios"].items()
                    for node in value["indicators"]}
    full_attempts = attempts[(attempts.evaluation_track == "primary_discovery") &
                             (attempts.method == "full_method")].copy()
    attempt_keys = ["scenario", "hypothesis_group_id", "parameter", "direction", "root_source",
                    "edge_source", "edge_target"]
    unique_keys(full_attempts, attempt_keys, "primary full-method intervention")
    attempt_lookup = full_attempts.set_index(attempt_keys)
    records, segments = [], []
    for scenario in SCENARIOS:
        subset = selected[selected.scenario == scenario].sort_values("path_id", kind="stable")
        for index, item in enumerate(subset.to_dict("records")):
            key = (scenario, item["path_id"])
            frozen, temporal_row = frozen_paths[key], temporal_lookup.loc[key]
            for field in ("parameter", "micro", "meso", "macro", "hypothesis_group_id"):
                if item[field] != temporal_row[field]:
                    raise ValueError(f"Stage 2/3 path identity mismatch: {key}, {field}")
            if frozen["parameter"] != item["parameter"] or frozen["intervention_direction"] != item["direction"]:
                raise ValueError(f"Frozen intervention identity mismatch: {key}")
            for scale in SCALES:
                if frozen[f"{scale}_indicator"] != item[scale]:
                    raise ValueError(f"Frozen path node mismatch: {key}, {scale}")
                node = frozen_nodes[(scenario, item[scale])]
                if node["scale"] != scale:
                    raise ValueError(f"Frozen scale mismatch: {key}, {scale}")
                item[f"{scale}_semantic_name"] = node["semantic_name"]
            for field in ("manipulation_success", "micro_significant", "meso_significant", "macro_significant",
                          "direction_supported", "onset_order_supported"):
                item[field] = saved_bool(item[field])
            if item["path_classification"] not in STATE_STYLES:
                raise ValueError(f"Unexpected saved path classification: {key}")
            code = f"{scenario[0].upper()}{index + 1:02d}"
            parameter_label = PARAMETER_LABELS.get(item["parameter"], item["parameter"].replace("_", " "))
            if item["direction"] not in {"plus", "minus"}:
                raise ValueError(f"Unexpected intervention direction: {key}")
            short_label = f"{parameter_label}{'+' if item['direction'] == 'plus' else '−'}"
            item.update(row=index, path_code=code, row_label=f"{code}  {short_label}",
                        parameter_label=short_label, holdout_classification="not_evaluated",
                        holdout_confirmed=False)
            if key in holdout_lookup.index:
                h = holdout_lookup.loc[key]
                for field in ("parameter", "direction", "micro", "meso", "macro", "hypothesis_group_id"):
                    if h[field] != item[field]:
                        raise ValueError(f"Holdout path identity mismatch: {key}, {field}")
                confirmed = saved_bool(h.holdout_confirmed)
                if confirmed != (h.classification == "confirmed") or not saved_bool(h.primary_result_unchanged):
                    raise ValueError(f"Inconsistent saved holdout result: {key}")
                item.update(holdout_classification=h.classification, holdout_confirmed=confirmed)
            item["display_holdout_star"] = item["path_classification"] == "supported" and item["holdout_confirmed"]
            item["root_manipulation_display"] = "supported" if item["manipulation_success"] else "manipulation_failure"
            root_identity = (scenario, item["hypothesis_group_id"], item["parameter"], item["direction"], item["micro"])
            for segment, (source_scale, target_scale, field) in enumerate(
                (("micro", "meso", "micro_meso_class"), ("meso", "macro", "meso_macro_class")), start=1):
                attempt_key = (*root_identity, item[source_scale], item[target_scale])
                if attempt_key not in attempt_lookup.index:
                    raise ValueError(f"Missing exact root/edge/direction intervention: {key}, {field}")
                attempt = attempt_lookup.loc[attempt_key]
                raw = item[field]
                # Validate against the exact saved attempt; do not aggregate or reclassify it.
                if raw != attempt.underlying_class or raw != attempt.primary_class or raw not in DISPLAY_STATES:
                    raise ValueError(f"Saved edge/path classification mismatch: {key}, {field}")
                if saved_bool(attempt.manipulation_success) != item["manipulation_success"]:
                    raise ValueError(f"Root manipulation mismatch: {key}, {field}")
                scope = attempt.intervention_scope
                if scope not in SCOPE_LABELS:
                    raise ValueError(f"Unknown intervention scope: {key}, {field}")
                item[f"{source_scale}_{target_scale}_scope"] = scope
                item[f"{source_scale}_{target_scale}_display"] = DISPLAY_STATES[raw]
                segments.append({"scenario": scenario, "path_id": item["path_id"], "path_code": code,
                    "row": index, "segment": segment, "source": item[source_scale], "target": item[target_scale],
                    "status_file": INPUTS[1], "status_field": field, "raw_status": raw,
                    "display_status": DISPLAY_STATES[raw], "intervention_scope": scope,
                    "scope_file": INPUTS[2], "root_source": item["micro"],
                    "parameter": item["parameter"], "direction": item["direction"],
                    "hypothesis_group_id": item["hypothesis_group_id"],
                    "attempt_underlying_class": attempt.underlying_class})
            if (item["micro_meso_scope"], item["meso_macro_scope"]) != ("direct_root", "upstream_mediated"):
                raise ValueError(f"This figure's root/mediated layout does not match saved scopes: {key}")
            item["parameter_marker"] = SCOPE_MARKERS[item["micro_meso_scope"]]
            segments.append({"scenario": scenario, "path_id": item["path_id"], "path_code": code,
                "row": index, "segment": 0, "source": item["parameter"], "target": item["micro"],
                "status_file": INPUTS[1], "status_field": "manipulation_success",
                "raw_status": item["manipulation_success"], "display_status": item["root_manipulation_display"],
                "intervention_scope": item["micro_meso_scope"], "scope_file": INPUTS[2],
                "root_source": item["micro"], "parameter": item["parameter"], "direction": item["direction"],
                "hypothesis_group_id": item["hypothesis_group_id"], "attempt_underlying_class": ""})
            records.append(item)
    rows = pd.DataFrame(records)
    if set(map(tuple, rows[keys].to_numpy())) != set(map(tuple, stage2[keys].to_numpy())):
        raise AssertionError("Not every and only temporal-qualified path was retained")
    segment_table = pd.DataFrame(segments)
    scenario_rank = {scenario: rank for rank, scenario in enumerate(SCENARIOS)}
    segment_table["scenario_rank"] = segment_table.scenario.map(scenario_rank)
    segment_table = segment_table.sort_values(["scenario_rank", "row", "segment"]).drop(columns="scenario_rank")
    audit = {scenario: {"path_count": int((rows.scenario == scenario).sum()),
        "path_ids_in_order": rows.loc[rows.scenario == scenario, "path_id"].tolist(),
        "final_status_counts": rows.loc[rows.scenario == scenario, "path_classification"].value_counts().to_dict(),
        "holdout_star_count": int(rows.loc[rows.scenario == scenario, "display_holdout_star"].sum())}
        for scenario in SCENARIOS}
    return rows, segment_table, audit


def render(run: Path, output: Path) -> dict:
    if output == run or run in output.parents:
        raise ValueError("Figure outputs must be outside the archived run")
    before = {name: sha256(run / name) for name in INPUTS}
    rows, segments, audit = load_evidence(run)
    # Give every real path the same vertical pitch; panel heights follow row counts.
    pitch, top, gap, bottom = 0.145, 0.57, 0.51, 0.31
    heights = [(audit[scenario]["path_count"] + 0.37) * pitch for scenario in SCENARIOS]
    height = top + sum(heights) + gap * (len(SCENARIOS) - 1) + bottom
    fig = plt.figure(figsize=(7.20, height))
    cursor = height - top
    final_texts = []
    for panel_index, scenario in enumerate(SCENARIOS):
        panel_height = heights[panel_index]
        ax = fig.add_axes([0.13, (cursor - panel_height) / height, 0.855, panel_height / height])
        cursor -= panel_height + gap
        letter = "ab"[panel_index]
        subset = rows[rows.scenario == scenario]
        for item in subset.to_dict("records"):
            row, code = item["row"], item["path_code"]
            # Much lighter than the old alternating bands, with the original layout intact.
            if row % 2 == 1:
                ax.axhspan(row - 0.46, row + 0.46, color="#F1F0EB", alpha=0.30, zorder=-2)
            path_segments = segments[(segments.scenario == scenario) & (segments.path_id == item["path_id"])]
            for segment in path_segments.itertuples(index=False):
                colour, style = STATE_STYLES[segment.display_status]
                ax.plot([segment.segment, segment.segment + 1], [row, row], color=colour, ls=style,
                    lw=1.95, alpha=0.94, solid_capstyle="round", zorder=1,
                    gid=f"{letter}-{code}-segment-{segment.segment}-{segment.display_status}")
            ax.scatter([0], [row], s=27, marker=item["parameter_marker"], facecolors="white",
                edgecolors=COLOURS["ink"], linewidths=0.85, zorder=3,
                gid=f"{letter}-{code}-parameter-{item['micro_meso_scope']}")
            for stage, scale in enumerate(SCALES, start=1):
                ax.scatter([stage], [row], s=27, facecolors="white", edgecolors=COLOURS["ink"], linewidths=0.85,
                    zorder=3, gid=f"{letter}-{code}-{scale}")
            state = item["path_classification"]
            colour, style = STATE_STYLES[state]
            ax.plot([3.18, 3.35], [row, row], color=colour, ls=style, lw=1.8,
                    solid_capstyle="round", gid=f"{letter}-{code}-final-{state}")
            text_colour = COLOURS["grey"] if state == "manipulation_failure" else colour
            final_texts.append(ax.text(3.41, row, STATE_LABELS[state], fontsize=5.5, color=text_colour,
                va="center", ha="left", gid=f"{letter}-{code}-final-label"))
            if item["display_holdout_star"]:
                ax.text(3.72, row, "*", fontsize=7, color=COLOURS["ink"], va="center", ha="center",
                        gid=f"{letter}-{code}-holdout-confirmed")
        ax.set_xticks(range(4), ["Parameter", "Micro", "Meso", "Macro"])
        ax.set_yticks(subset.row, subset.row_label, fontsize=6.0)
        ax.set_ylim(len(subset) - 0.45, -0.82)
        ax.set_xlim(-0.15, 4.16)
        scope_labels = []
        for column in ("micro_meso_scope", "meso_macro_scope"):
            scopes = subset[column].unique()
            if len(scopes) != 1:
                raise ValueError("Mixed intervention scopes need explicit per-row scope annotations")
            scope_labels.append(SCOPE_LABELS[scopes[0]])
        for x, label in zip((0.5, 1.5, 2.5, 3.62), ("Root manipulation", *scope_labels, "Path status")):
            ax.text(x, 1.015, label, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
                    fontsize=5.8, color=COLOURS["grey"])
        ax.set_title(f"{scenario.capitalize()}: temporal-qualified paths  n={len(subset)}", fontsize=7.5, pad=15)
        ax.tick_params(length=3.0, width=0.9, labelsize=6.2, pad=2)
        ax.text(-0.11, 1.06, letter, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top")
    handles = [Line2D([0], [0], color=colour, ls=style, lw=1.8,
        label=state.replace("_", " ")) for state, (colour, style) in STATE_STYLES.items()]
    fig.legend(handles=handles, loc="upper center", ncol=4, bbox_to_anchor=(0.53, 0.998),
        fontsize=5.5, columnspacing=1.4, handlelength=2.6, handletextpad=0.45)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    if any(not fig.bbox.contains(*text.get_window_extent(renderer).get_points()[1]) for text in final_texts):
        raise AssertionError("A path-status label lies outside the figure")
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
    row_path = source_dir / "figure_7_path_codebook.tsv"
    segment_path = source_dir / "figure_7_plotted_segments.tsv"
    rows.to_csv(row_path, sep="\t", index=False, na_rep="NA")
    segments.to_csv(segment_path, sep="\t", index=False, na_rep="NA")
    caption = (
        "Figure 7. Segment-wise propagation evidence for every Stage 2 temporal-qualified candidate path: "
        + "; ".join(f"{scenario.capitalize()} ({'ab'[i]}), n={audit[scenario]['path_count']}" for i, scenario in enumerate(SCENARIOS))
        + ". Rows follow ascending path_id within each scenario, with no effect-magnitude ranking or top-k selection. "
        "Each row follows Parameter → Micro → Meso → Macro. The first segment displays the saved "
        "manipulation_success flag (true: supported root manipulation; false: manipulation failure). "
        "The next two segments use the saved micro_meso_class and meso_macro_class, respectively. "
        "For the four-category display only, no_stable_downstream_effect shares the inconclusive style; "
        "the original classification remains available in the source tables. No classifications are recomputed. "
        "A single open square at Parameter identifies the direct Micro-root intervention, replacing the former "
        "double-circle symbol. Exact saved intervention_scope fields identify Micro→Meso evidence as direct_root "
        "and Meso→Macro evidence as upstream_mediated; the latter does not represent direct manipulation of Meso. "
        "All Parameter, Micro, Meso and Macro nodes have neutral white fills and dark-grey borders; "
        "node colour does not encode scale, significance or evidence status. Evidence is encoded by "
        "connections: supported uses blue solid lines, contradicted red dashed lines, inconclusive "
        "dark-grey dashed lines, and manipulation failure light-grey dotted lines. "
        "The rightmost status is the saved path_classification, independent of the segment display. "
        "Supported segments can coexist with a contradicted complete path when the frozen path's required "
        "response directions fail; this distinction is preserved. "
        "A small * after a supported final status indicates saved holdout confirmation "
        + "(" + "; ".join(f"{scenario.capitalize()}: {audit[scenario]['holdout_star_count']}" for scenario in SCENARIOS) + "). "
        "Holdout is an auxiliary annotation and does not redefine primary support. "
        "Dest = destination preference; Move = move probability; Tol = tolerance; AS = assimilation strength; "
        "BT = backfire threshold; CB = confidence bound; +/− are the saved intervention directions. "
        "S/D path codes identify sorted paths and map to complete frozen node IDs and semantic names in "
        "source_data/figure_7_path_codebook.tsv. The three displayed segments and their exact source fields "
        "are supplied in source_data/figure_7_plotted_segments.tsv.\n\nInputs:\n"
        + "".join(f"- `{name}`\n" for name in INPUTS)
    )
    (output / "figure_7_caption.md").write_text(caption, encoding="utf-8")
    if before != {name: sha256(run / name) for name in INPUTS}:
        raise RuntimeError("A source artifact changed during rendering")
    report = {"status": "passed", "source_run": str(run), "source_sha256": before,
        "selection_rule": "all path_temporally_qualified == True; ascending path_id within scenario",
        "panels": audit, "path_count": len(rows), "segment_count": len(segments),
        "display_status_mapping": DISPLAY_STATES, "parameter_marker": "single open square for direct_root",
        "node_style": {"fill": "white", "edge": COLOURS["ink"], "significance_encoded": False},
        "scope_counts": segments.loc[segments.segment.gt(0), "intervention_scope"].value_counts().to_dict(),
        "segment_raw_status_counts": {str(k): int(v) for k, v in segments.raw_status.value_counts().items()},
        "row_pitch_inches": pitch, "figure_inches": [7.2, height], "legend_count": 1,
        "classification_recomputed": False, "experiment_recalculation": False, "input_unchanged": True,
        "script_sha256": sha256(Path(__file__)), "outputs": {path.name: sha256(path) for path in exports},
        "source_tables": {path.name: sha256(path) for path in (row_path, segment_path)}}
    (qa_dir / "figure_7_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path,
        default=Path(__file__).resolve().parents[1] / "runs" / "baoba20260904_01")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = render(args.run.resolve(), args.output_dir.resolve())
    print(json.dumps({key: result[key] for key in ("status", "panels", "segment_count", "scope_counts", "outputs")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
