"""Figure 12: saved observational versus intervention timing, without new gates."""
from figure_9_12_helpers import *
from matplotlib.ticker import MaxNLocator

INPUTS = ("analysis/path_timing_concordance.csv", "analysis/path_temporal_qualification.csv")
CLASS_MARKERS = {"supported": ("o", 6.2), "contradicted": ("x", 4.6),
                 "inconclusive": ("^", 4.8), "manipulation_failure": ("s", 4.0)}

def render(run, output):
    style(12)
    before = hashes(run, INPUTS)
    data = pd.read_csv(run/INPUTS[0])
    temporal = pd.read_csv(run/INPUTS[1], usecols=["scenario", "path_id", "path_temporally_qualified"])
    keys = ["scenario", "path_id"]
    unique(data, keys); unique(temporal, keys)
    qualified = temporal[temporal.path_temporally_qualified.map(boolean)]
    wanted = set(map(tuple, qualified[keys].to_numpy()))
    selected = qualified[keys].merge(data, on=keys, how="left", validate="one_to_one", indicator=True)
    if not selected._merge.eq("both").all():
        raise ValueError("A Stage 2-qualified path has no saved timing-concordance row")
    selected = selected.drop(columns="_merge").sort_values(keys)
    if set(map(tuple, selected[keys].to_numpy())) != wanted:
        raise ValueError("Incomplete temporal-qualified path selection")
    if set(selected.scenario) != set(SCENARIOS) or not selected.path_classification.isin(CLASS_MARKERS).all():
        raise ValueError("Unexpected scenario or classification")
    panels = [("a", "Micro→Meso", "micro_meso_observational_lag", "micro_meso_intervention_delay"),
              ("b", "Meso→Macro", "meso_macro_observational_lag", "meso_macro_intervention_delay")]
    # Accept the equivalent saved field spelling; never calculate or synthesize a total.
    total_x = next((name for name in ("total_observational_lag", "observational_total_lag") if name in data), None)
    if total_x is not None and "intervention_total_latency" in data:
        panels.append(("c", "Total timing", total_x, "intervention_total_latency"))
    fig, axes = plt.subplots(1, len(panels), figsize=(2.8*len(panels), 3.30), squeeze=False)
    fig.subplots_adjust(left=.075, right=.99, bottom=.18, top=.72, wspace=.30)
    scenario_legend(fig, y=1.0, line=False)
    class_handles = [Line2D([0],[0],ls="None",marker=marker,ms=size,mfc="none",mec=COLOURS["ink"],
        mew=1.0,label=state.replace("_", " ")) for state,(marker,size) in CLASS_MARKERS.items()]
    fig.legend(handles=class_handles, loc="upper center", bbox_to_anchor=(.5,.925), ncol=4,
               fontsize=6.1, columnspacing=1.5, handletextpad=.4)
    records, panel_audit = [], {}
    for ax, (letter, title, xcol, ycol) in zip(axes.flat, panels):
        xy = selected[[xcol,ycol]].to_numpy(float)
        if np.isinf(xy).any():
            raise ValueError("Infinite saved timing value")
        finite = np.isfinite(xy).all(axis=1)
        plotted = selected.loc[finite]
        missing = selected.loc[~finite]
        x_values, y_values = plotted[xcol].to_numpy(float), plotted[ycol].to_numpy(float)
        if not len(plotted):
            raise ValueError("No defined timing pairs in a requested panel")
        xmin, xmax = min(0., float(x_values.min())), float(x_values.max())
        ymin, ymax = min(0., float(y_values.min())), max(float(y_values.max()), xmax)
        xpad, ypad = .08*max(xmax-xmin,1.), .10*max(ymax-ymin,1.)
        ax.set_xlim(xmin-xpad,xmax+xpad); ax.set_ylim(ymin-ypad,ymax+ypad)
        reference_x = np.array([xmin-xpad, xmax+xpad])
        ax.plot(reference_x,reference_x,color="#9CA3A7",lw=.8,ls=(0,(3,3)),zorder=0,gid=f"{letter}-equality-reference")
        ax.annotate("y = x", xy=(xmax,xmax), xytext=(-1,5), textcoords="offset points", ha="right",
                    fontsize=5.5,color=COLOURS["grey"])
        # Draw every path at its exact saved coordinates. No jitter or support-based exclusion.
        for index, row in enumerate(selected.to_dict("records")):
            marker, size = CLASS_MARKERS[row["path_classification"]]
            valid = bool(np.isfinite(row[xcol]) and np.isfinite(row[ycol]))
            if valid:
                ax.plot([row[xcol]],[row[ycol]],ls="None",marker=marker,ms=size,mfc="none",
                    mec=COLOURS[row["scenario"]],mew=1.15,zorder=3,
                    gid=f"{letter}-path-{index}-{row['scenario']}-{row['path_classification']}")
            records.append({"panel":letter,"scenario":row["scenario"],"path_id":row["path_id"],
                "path_classification":row["path_classification"],"x_field":xcol,"y_field":ycol,
                "x":row[xcol],"y":row[ycol],"plotted":valid,"source_file":INPUTS[0]})
        coincident = plotted.groupby(["scenario","path_classification",xcol,ycol]).size()
        for (scenario, state, x, y), count in coincident.items():
            if count > 1:
                ax.annotate(str(count),xy=(x,y),xytext=(5,-8),textcoords="offset points",
                    fontsize=5.2,color=COLOURS[scenario],gid=f"{letter}-coincident-{scenario}-{state}-{x}-{y}")
        ax.set_xlabel("Observational total lag" if letter=="c" else "Observational lag",fontsize=6.5)
        ax.set_ylabel("Intervention total latency" if letter=="c" else "Intervention delay",fontsize=6.5)
        ax.set_title(title,fontsize=7.2,pad=9)
        ax.text(.98,.98,f"{len(plotted)}/{len(selected)} defined",transform=ax.transAxes,
            ha="right",va="top",fontsize=5.6,color=COLOURS["grey"])
        ax.xaxis.set_major_locator(MaxNLocator(nbins=4,integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=4,integer=True))
        axes_style(ax,letter)
        panel_audit[letter] = {"title":title,"x_field":xcol,"y_field":ycol,"eligible_paths":len(selected),
            "finite_pairs":len(plotted),"missing_pairs":len(missing),
            "finite_by_scenario":plotted.groupby("scenario").size().to_dict(),
            "missing_by_scenario":missing.groupby("scenario").size().to_dict(),
            "negative_delays":int((y_values<0).sum()),"supported_plotted":int(plotted.path_classification.eq("supported").sum()),
            "x_limits":list(ax.get_xlim()),"y_limits":list(ax.get_ylim())}
    caption = (
        "Figure 12. Observational timing versus intervention timing for all Stage 2 temporal-qualified paths. "
        "Panels a/b compare the saved Micro→Meso and Meso→Macro observational lag with the corresponding "
        "saved intervention delay. "
        + (f"Panel c uses the existing {total_x} and intervention_total_latency fields. " if len(panels)==3 else "")
        + "Blue denotes Schelling and red Deffuant. Marker shapes identify the saved path_classification: "
        "circle, supported; cross, contradicted; triangle, inconclusive; square, manipulation failure. "
        "Each finite path is plotted at its exact saved coordinates without jitter, averaging, sign filtering "
        "or classification changes. Small numerals identify coincident paths sharing a scenario, classification "
        "and coordinate pair. Negative delays are retained. The y=x line is a visual reference only, not a "
        "Stage 3 v2 hard gate; supported paths are retained regardless of timing agreement. Undefined coordinate "
        "pairs stay NaN in the full source table and cannot produce a plotted point. "
        + " ".join(f"Panel {letter}: {info['finite_pairs']}/{info['eligible_paths']} finite pairs, {info['missing_pairs']} missing." for letter,info in panel_audit.items())
        + f" The selected set contains {int(selected.path_classification.eq('supported').sum())} supported paths; "
        "each panel includes every one with defined coordinates. "
        "The temporal-qualification table is used only to select/verify path membership; all plotted coordinates "
        "and classifications come directly from path_timing_concordance.csv.\n\nInputs:\n"
        + "".join(f"- `{name}`\n" for name in INPUTS))
    return finish(fig,12,"figure_12_timing_concordance",run,output,before,
        {"figure_12_plotted_coordinates.tsv":pd.DataFrame(records),"figure_12_qualified_path_records.tsv":selected},caption,
        {"eligible_paths":len(selected),"eligible_by_scenario":selected.groupby("scenario").size().to_dict(),
         "panels":panel_audit,"statistic":"unaggregated saved coordinates","timing_equality_gate":False,
         "coordinate_jitter":False,"total_observational_field":total_x},__file__)

if __name__ == "__main__":
    render(*arguments(__doc__))
