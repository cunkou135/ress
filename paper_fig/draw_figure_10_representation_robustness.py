"""Figure 10: representation-error robustness from saved repeated results."""
from figure_9_12_helpers import *

INPUTS = ("analysis/representation_robustness.csv",)
OPERATORS = ("irrelevant_indicator", "redundant_semantic_indicator", "delete_candidate_relation",
             "wrong_hypothesis_group_assignment", "cross_hypothesis_group_relation")
TITLES = ("Irrelevant\nindicator", "Redundant semantic\nindicator", "Delete candidate\nrelation",
          "Wrong hypothesis\ngroup assignment", "Cross-hypothesis\ngroup relation")
METRICS = ("temporal_qualification_rate", "stability")

def render(run, output):
    style(10)
    before = hashes(run, INPUTS)
    data = pd.read_csv(run/INPUTS[0], usecols=["scenario", "operator", "error_ratio", "repetition",
        "evaluation_track", "candidate_edge_count", "retained_edge_count", *METRICS])
    unique(data, ["scenario", "operator", "error_ratio", "repetition"])
    if set(data.operator) != set(OPERATORS) or set(data.scenario) != set(SCENARIOS):
        raise ValueError("Unexpected scenario/operator set")
    if not data.evaluation_track.eq("full_discovery").all():
        raise ValueError("Unexpected evaluation track")
    np.testing.assert_allclose(data.temporal_qualification_rate,
        data.retained_edge_count/data.candidate_edge_count, equal_nan=True)
    records = []
    for (scenario, operator, ratio), group in data.groupby(["scenario", "operator", "error_ratio"]):
        for metric in METRICS:
            values = group[metric].to_numpy(float)
            if np.isinf(values).any():
                raise ValueError("Infinite saved robustness value")
            finite = values[np.isfinite(values)]
            median = float(np.median(finite)) if len(finite) else np.nan
            q25, q75 = np.quantile(finite, [.25, .75], method="linear") if len(finite) > 1 else (np.nan, np.nan)
            row = METRICS.index(metric); col = OPERATORS.index(operator)
            records.append({"panel": "abcdefghij"[row*5+col], "scenario": scenario, "operator": operator,
                "error_ratio": ratio, "metric": metric, "n_total": len(values), "n_finite": len(finite),
                "median": median, "q25": q25, "q75": q75,
                "repetitions": json.dumps(sorted(group.repetition.tolist()))})
    summary = pd.DataFrame(records).sort_values(["panel", "scenario", "error_ratio"])
    fig, axes = plt.subplots(2, 5, figsize=(8.70, 3.35), sharex=True, sharey="row")
    fig.subplots_adjust(left=.075, right=.99, bottom=.14, top=.76, wspace=.18, hspace=.42)
    scenario_legend(fig)
    limits = {}
    for row, metric in enumerate(METRICS):
        values = summary.loc[summary.metric.eq(metric), ["median", "q25", "q75"]].to_numpy(float).ravel()
        values = values[np.isfinite(values)]
        span = max(float(np.ptp(values)), .02)
        low, high = max(0, float(values.min())-.1*span), min(1, float(values.max())+.1*span)
        limits[metric] = [low, high]
        for col, operator in enumerate(OPERATORS):
            ax = axes[row, col]; letter = "abcdefghij"[row*5+col]
            for scenario in SCENARIOS:
                g = summary[(summary.metric==metric)&(summary.operator==operator)&(summary.scenario==scenario)].sort_values("error_ratio")
                if g.empty:
                    raise ValueError("Missing requested series")
                x, y, q25, q75 = [g[name].to_numpy(float) for name in ("error_ratio", "median", "q25", "q75")]
                ax.fill_between(x, q25, q75, where=np.isfinite(q25)&np.isfinite(q75), color=COLOURS[scenario],
                                alpha=.10, lw=0, gid=f"{letter}-{scenario}-iqr")
                ax.plot(x, y, color=COLOURS[scenario], marker="o", ms=2.8, lw=1.75,
                        solid_capstyle="round", gid=f"{letter}-{scenario}-median")
            ax.set_ylim(low, high)
            xs = np.sort(data.loc[data.operator.eq(operator), "error_ratio"].unique())
            pad = .05*max(float(np.ptp(xs)), .1)
            ax.set_xlim(float(xs.min())-pad, float(xs.max())+pad)
            ax.set_xticks(xs[np.unique(np.round(np.linspace(0, len(xs)-1, min(3, len(xs)))).astype(int))])
            if row==0:
                ax.set_title(TITLES[col], fontsize=6.6, pad=20)
            else:
                ax.set_xlabel("Error ratio", fontsize=6.2)
            if col==0:
                ax.set_ylabel("Temporal\nqualification rate" if row==0 else "Stability", fontsize=6.2)
            axes_style(ax, letter)
    counts = sorted(summary.n_total.unique().tolist())
    caption = (
        "Figure 10. Stage 1 representation-error robustness. Columns, left to right, correspond to "
        + ", ".join(OPERATORS) + ". The upper row shows retained candidate relations / total candidate "
        "relations (temporal qualification rate); the lower row shows the saved stability metric. "
        "Blue denotes Schelling and red Deffuant. Within each scenario × operator × error_ratio, lines are "
        "the repetition median and shading is the 25th–75th percentile IQR (linear interpolation), describing "
        f"between-repetition variability. Saved repetitions per condition: {counts}. "
        "All error ratios and all requested operators are retained. Each operator keeps its own zero-error "
        "records. Undefined values remain missing. Full repeat-level rows and plotted summaries are supplied "
        "in the accompanying source tables. No reference-recovery metric is computed.\n\n"
        f"Input: `{INPUTS[0]}`.\n"
    )
    return finish(fig, 10, "figure_10_representation_robustness", run, output, before,
        {"figure_10_plotted_summary.tsv": summary, "figure_10_saved_repetitions.tsv": data}, caption,
        {"input_rows": len(data), "condition_count": data.groupby(["scenario","operator","error_ratio"]).ngroups,
         "summary_points": len(summary), "repetitions_per_condition": counts, "y_limits": limits,
         "statistic": "median and IQR across saved repetitions", "missing_metrics": data[list(METRICS)].isna().sum().to_dict()}, __file__)

if __name__ == "__main__":
    render(*arguments(__doc__))
