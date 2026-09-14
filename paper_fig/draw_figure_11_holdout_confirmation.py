"""Figure 11: dynamically counted path funnel and path-level holdout matrix."""
from figure_9_12_helpers import *
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator

INPUTS = ("representation/candidate_paths.json", "analysis/path_temporal_qualification.csv",
          "analysis/path_intervention_classification.csv", "analysis/holdout_path_confirmation.csv")
STAGES = ("Candidate paths", "Temporal-qualified paths", "Primary-supported paths", "Holdout-confirmed paths")
PARAMETERS = {"tolerance": "Tol", "confidence_bound": "CB"}
OUTCOMES = {"macro_global_spatial_neighbor_similarity": "spatial sim.",
    "macro_global_connected_components": "components", "macro_global_moved_fraction": "relocation",
    "macro_network_assortativity": "assortativity", "macro_opinion_global_variance": "global var."}

def render(run, output):
    style(11)
    before = hashes(run, INPUTS)
    candidates = json.loads((run/INPUTS[0]).read_text(encoding="utf-8"))["scenarios"]
    temporal, primary, holdout = [pd.read_csv(run/name) for name in INPUTS[1:]]
    keys = ["scenario", "path_id"]
    for frame in (temporal, primary, holdout):
        unique(frame, keys)
    if set(candidates) != set(SCENARIOS):
        raise ValueError("Unexpected frozen scenario set")
    frozen = {(s, path["path_id"]): path for s, paths in candidates.items() for path in paths}
    if len(frozen) != sum(len(v) for v in candidates.values()):
        raise ValueError("Duplicate frozen path")
    if set(map(tuple, temporal[keys].to_numpy())) != set(frozen) or set(map(tuple, primary[keys].to_numpy())) != set(frozen):
        raise ValueError("Frozen candidates and Stage 2/3 path inventories differ")
    t, p, h = (frame.set_index(keys) for frame in (temporal, primary, holdout))
    if not holdout.evaluation_track.eq("holdout_confirmation").all():
        raise ValueError("Unexpected holdout track")
    membership, matrix_rows, counts = [], [], []
    for scenario in SCENARIOS:
        supported_index = 0
        for key in sorted(k for k in frozen if k[0]==scenario):
            candidate, stage2, stage3 = frozen[key], t.loc[key], p.loc[key]
            for field in ("parameter", "micro", "meso", "macro"):
                frozen_field = field if field=="parameter" else f"{field}_indicator"
                if stage2[field] != candidate[frozen_field] or stage3[field] != candidate[frozen_field]:
                    raise ValueError(f"Saved path identity mismatch: {key}, {field}")
            if stage3.direction != candidate["intervention_direction"]:
                raise ValueError("Saved intervention direction mismatch")
            qualified = boolean(stage2.path_temporally_qualified)
            supported = stage3.path_classification == "supported"
            if qualified != boolean(stage3.path_temporally_qualified) or (supported and not qualified):
                raise ValueError("Saved stage membership is inconsistent")
            hclass, confirmed = np.nan, False
            if key in h.index:
                hold = h.loc[key]
                for field in ("parameter", "direction", "micro", "meso", "macro"):
                    if hold[field] != stage3[field]:
                        raise ValueError("Holdout path identity mismatch")
                hclass = hold.classification
                confirmed = boolean(hold.holdout_confirmed)
                if confirmed != (hclass=="confirmed") or not boolean(hold.primary_result_unchanged):
                    raise ValueError("Inconsistent saved holdout status")
                if not supported:
                    raise ValueError("Holdout contains a path outside primary support")
            membership.append({"scenario": scenario, "path_id": key[1], "candidate": True,
                "temporal_qualified": qualified, "primary_supported": supported,
                "primary_classification": stage3.path_classification, "holdout_status": hclass,
                "holdout_confirmed": confirmed if key in h.index else pd.NA,
                "holdout_evaluated": key in h.index})
            if supported:
                supported_index += 1
                parameter = PARAMETERS.get(stage3.parameter, stage3.parameter.replace("_", " "))
                direction = {"plus": "+", "minus": "−"}[stage3.direction]
                outcome = OUTCOMES.get(stage3.macro, stage3.macro.replace("macro_", "").replace("_", " "))
                code = f"{scenario[0].upper()}{supported_index:02d}"
                matrix_rows.append({"scenario": scenario, "path_code": code, "path_id": key[1],
                    "path_label": f"{code}  {parameter}{direction} | {outcome}",
                    "primary_classification": stage3.path_classification, "holdout_status": hclass,
                    "holdout_confirmed": confirmed if key in h.index else pd.NA})
        members = [m for m in membership if m["scenario"]==scenario]
        numbers = (len(members), sum(m["temporal_qualified"] for m in members),
            sum(m["primary_supported"] for m in members),
            sum(m["holdout_status"]=="confirmed" for m in members))
        for stage_index, (label, count) in enumerate(zip(STAGES, numbers)):
            counts.append({"scenario": scenario, "stage_index": stage_index, "stage": label, "path_count": count})
    if not set(h.index).issubset(set(frozen)):
        raise ValueError("Unmatched holdout path")
    count_table, matrix = pd.DataFrame(counts), pd.DataFrame(matrix_rows)
    fig, (ax, table_ax) = plt.subplots(1, 2, figsize=(9.00, 3.25), gridspec_kw={"width_ratios": [32, 68]})
    fig.subplots_adjust(left=.135, right=.992, top=.80, bottom=.14, wspace=.34)
    scenario_legend(fig, line=False)
    for scenario, offset in zip(SCENARIOS, (-.16, .16)):
        g = count_table[count_table.scenario==scenario].sort_values("stage_index")
        for item in g.itertuples(index=False):
            ax.barh(item.stage_index+offset, item.path_count, height=.27, color=COLOURS[scenario],
                    zorder=3, gid=f"a-{scenario}-stage-{item.stage_index}")
            ax.text(item.path_count+.25, item.stage_index+offset, str(item.path_count),
                    fontsize=6.2, va="center", color=COLOURS[scenario])
    ax.set_yticks(range(4), ["Candidate\npaths", "Temporal-qualified\npaths", "Primary-supported\npaths", "Holdout-confirmed\npaths"])
    ax.set_ylim(3.5, -.5)
    ax.set_xlim(0, float(count_table.path_count.max())*1.18)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
    ax.set_xlabel("Number of paths", fontsize=6.5)
    ax.set_title("Path funnel", fontsize=7.5, pad=8)
    axes_style(ax, "a", grid="x"); ax.tick_params(axis="y", length=0)
    table_ax.set_xlim(0, 1); table_ax.set_ylim(len(matrix)-.5, -1.1)
    table_ax.axis("off")
    table_ax.set_title("Holdout confirmation matrix", fontsize=7.5, pad=8)
    axes_style(table_ax, "b", grid="")
    columns = ((.015, "Scenario"), (.185, "Path"), (.61, "Primary\nclassification"), (.815, "Holdout\nconfirmation"))
    for x, title in columns:
        table_ax.text(x, -.78, title, va="center", fontsize=6.3, fontweight="bold", color=COLOURS["ink"])
    for index, row in enumerate(matrix.itertuples(index=False)):
        if index%2:
            table_ax.add_patch(Rectangle((0,index-.45), 1, .9, facecolor="#F1F0EB", alpha=.45, lw=0))
        table_ax.axhline(index+.5, color=COLOURS["grid"], lw=.4, alpha=.7)
        table_ax.text(.015, index, row.scenario.capitalize(), va="center", fontsize=6, color=COLOURS[row.scenario])
        table_ax.text(.185, index, row.path_label, va="center", fontsize=6, color=COLOURS["ink"])
        table_ax.text(.61, index, row.primary_classification.capitalize(), va="center", fontsize=6, color=COLOURS["ink"])
        value = row.holdout_status.capitalize() if pd.notna(row.holdout_status) else "NA"
        table_ax.text(.815, index, value, va="center", fontsize=6,
            fontweight="bold" if row.holdout_status=="confirmed" else "normal",
            color=COLOURS["ink"] if row.holdout_status=="confirmed" else COLOURS["grey"])
    caption = (
        "Figure 11. Primary-to-holdout path confirmation. Panel a counts frozen candidates, saved "
        "path_temporally_qualified=True paths, saved path_classification=supported paths, and their saved "
        "holdout_confirmed=True paths, respectively. Counts are derived by exact scenario/path_id joins, "
        "with no reconstructed classification. "
        + " ".join(f"{scenario.capitalize()}: " + " → ".join(map(str, count_table.loc[count_table.scenario==scenario,'path_count'])) + "." for scenario in SCENARIOS)
        + " Panel b includes every Primary supported path and reports its saved path-level holdout classification. "
        "Holdout outcomes do not alter Primary classifications. Short labels affect text only; complete path IDs "
        "and exact statuses are in source_data/figure_11_confirmation_matrix.tsv. Tol and CB abbreviate tolerance "
        "and confidence bound; +/− indicate the saved intervention direction. No edge-level holdout conclusions "
        "are inferred. These are deterministic path counts, without averaging or uncertainty intervals.\n\nInputs:\n"
        + "".join(f"- `{name}`\n" for name in INPUTS))
    return finish(fig, 11, "figure_11_holdout_confirmation", run, output, before,
        {"figure_11_path_funnel.tsv": count_table, "figure_11_confirmation_matrix.tsv": matrix,
         "figure_11_path_membership.tsv": pd.DataFrame(membership)}, caption,
        {"candidate_count": len(frozen), "primary_supported_matrix_rows": len(matrix),
         "funnel": {s: count_table.loc[count_table.scenario==s,"path_count"].tolist() for s in SCENARIOS},
         "holdout_rows": len(holdout), "statistic": "exact saved path membership counts"}, __file__)

if __name__ == "__main__":
    render(*arguments(__doc__))

