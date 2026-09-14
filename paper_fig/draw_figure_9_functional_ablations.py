"""Figure 9: saved method-component ablations, with undefined values left missing."""
from figure_9_12_helpers import *

INPUTS = ("analysis/functional_ablations.csv",)
VARIANTS = ("full_method", "without_joint_trajectories", "without_bootstrap",
            "without_structured_representation", "without_paired_seeds")
LABELS = ("Full method", "Without joint\ntrajectories", "Without bootstrap",
          "Without structured\nrepresentation", "Without paired seeds")
METRICS = ("stability", "intervention_support_rate", "mean_ci_width")
TITLES = ("Stability", "Intervention support rate", "Mean CI width")

def render(run, output):
    style(9)
    before = hashes(run, INPUTS)
    raw = pd.read_csv(run/INPUTS[0], usecols=["scenario", "variant", "evaluation_track", *METRICS])
    selected = raw[raw.variant.isin(VARIANTS)].copy()
    unique(selected, ["scenario", "variant"])
    if set(map(tuple, selected[["scenario", "variant"]].to_numpy())) != {(s, v) for s in SCENARIOS for v in VARIANTS}:
        raise ValueError("Missing requested scenario/variant combinations")
    if not selected.evaluation_track.eq("full_discovery").all():
        raise ValueError("Unexpected evaluation track")
    if np.isinf(selected[list(METRICS)].to_numpy(float)).any():
        raise ValueError("Infinite saved ablation value")
    fig, axes = plt.subplots(1, 3, figsize=(7.20, 2.65), sharey=True)
    fig.subplots_adjust(left=.225, right=.985, top=.76, bottom=.14, wspace=.37)
    scenario_legend(fig, line=False)
    records, audit = [], {}
    for ax, letter, metric, title in zip(axes, "abc", METRICS, TITLES):
        for scenario, offset in zip(SCENARIOS, (-.12, .12)):
            values = selected[selected.scenario.eq(scenario)].set_index("variant").loc[list(VARIANTS), metric]
            for index, (variant, value) in enumerate(values.items()):
                finite = bool(np.isfinite(value))
                if finite:
                    ax.plot(value, index+offset, ls="None", marker="o", ms=4.5,
                        color=COLOURS[scenario], gid=f"{letter}-{scenario}-{variant}")
                records.append({"panel": letter, "scenario": scenario, "variant": variant, "metric": metric,
                    "value": value, "defined": finite, "display_y": index+offset, "source_file": INPUTS[0]})
        values = selected[metric].dropna().to_numpy(float)
        if not len(values):
            ax.text(.5, .5, "No defined values", transform=ax.transAxes, ha="center", color=COLOURS["grey"], fontsize=6)
        else:
            lo, hi = float(values.min()), float(values.max())
            pad = max(.14*(hi-lo), .015 if metric != "mean_ci_width" else .01)
            ax.set_xlim(max(0, lo-pad), min(1, hi+pad) if metric != "mean_ci_width" else hi+pad)
        ax.set_ylim(len(VARIANTS)-.52, -.52)
        ax.set_yticks(np.arange(len(VARIANTS)), LABELS, fontsize=6.1)
        ax.set_title(title, fontsize=7, pad=8)
        axes_style(ax, letter, grid="x")
        ax.tick_params(axis="y", length=0)
        audit[letter] = {"metric": metric, "records": len(selected), "defined": int(selected[metric].notna().sum()),
            "missing": selected.loc[selected[metric].isna(), ["scenario", "variant"]].to_dict("records")}
    caption = (
        "Figure 9. Method-component ablations. Panels a–c show saved stability, intervention_support_rate "
        "and mean_ci_width, respectively. Blue denotes Schelling and red Deffuant. Each point is one "
        "saved scenario × variant summary, with no repeat-level aggregation or added uncertainty interval. "
        "Mean CI width is itself the saved outcome metric, not an error bar on this plot. Empty positions "
        "retain the CSV's undefined values. Only the five requested variants are included, in the stated order. "
        "Intervention support rate is the saved intervention-evidence metric, not a newly inferred path-level "
        "support fraction. Full labels map directly to the variant IDs in source_data/figure_9_plotted_values.tsv.\n\n"
        f"Input: `{INPUTS[0]}`.\n\nUndefined records:\n"
        + "".join(f"- {row['scenario']} / {row['variant']} / {row['metric']}\n" for row in records if not row["defined"])
    )
    return finish(fig, 9, "figure_9_functional_ablations", run, output, before,
        {"figure_9_plotted_values.tsv": pd.DataFrame(records)}, caption,
        {"input_rows": len(raw), "selected_rows": len(selected), "variants": list(VARIANTS), "panels": audit,
         "statistic": "saved summary value; no new averaging", "uncertainty_added": False}, __file__)

if __name__ == "__main__":
    render(*arguments(__doc__))
