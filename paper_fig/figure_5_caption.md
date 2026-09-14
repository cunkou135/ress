Figure 5. Mean intervention effect trajectories and propagation timelines of Stage 3-supported paths. Panels a and c show Schelling and Deffuant, respectively, at simulation times 0-30. Representatives are taken directly from the saved representative-path selection; their saved IDs and holdout status are listed below. Curves show the saved primary-discovery mean standardised paired effect, with the saved bootstrap interval bounds as shading. Blue solid, blue dashed and red solid lines denote Micro, Meso and Macro, respectively; each response panel has a complete three-curve legend centred below it. Dotted vertical lines mark the saved onsets and every line is directly labelled; coincident scale onsets share one combined label. Text for nearby onsets is staggered across the upper plot edge while onset-line coordinates remain unchanged. Panels b and d include every path whose final primary path_classification is supported, without additional selection by onset order, significance or holdout outcome. Each path uses its saved Micro onset as time zero: x_micro = 0, x_meso = meso_onset − micro_onset, and x_macro = macro_onset − micro_onset. The blue segment runs from x_micro to x_meso and the red segment runs continuously from x_meso to x_macro. Their lengths are the Micro→Meso and Meso→Macro delays, respectively; the second delay is not used as a separate position measured from zero. Blue hollow circles mark Micro/Meso and a small red square marks Macro. Coincident onsets retain zero-length segments and overlapping markers without horizontal or vertical jitter; the smaller red square sits inside the blue circle when their onsets coincide. Absolute-onset uncertainty bounds are not reused as relative-onset or delay intervals, and no delay uncertainty is inferred or drawn. Bold path labels identify the representative shown on the left. Tol and CB abbreviate tolerance and confidence_bound; minus and plus denote the saved intervention direction. Intervals, support classifications and onset detection are not recomputed.

Supported paths: Schelling n=3; Deffuant n=3.

| Scenario | Short label | Saved path ID | Micro → Meso → Macro onset | Micro→Meso delay | Meso→Macro delay | Representative | Holdout confirmed |
|---|---|---|---|---|---|---|---|
| Schelling | Tol− / spatial sim. | `tol_minus_unhappy_to_move_std_to_spatial_sim` | 0 → 0 → 1 | 0 | 1 | True | True |
| Schelling | Tol− / components | `tol_minus_unhappy_to_unhappy_std_to_components` | 0 → 0 → 2 | 0 | 2 | False | True |
| Schelling | Tol+ / relocation | `tol_plus_unhappy_to_move_std_to_global_moved` | 0 → 0 → 0 | 0 | 0 | False | False |
| Deffuant | CB− / assortativity | `cb_minus_accept_absovar_assort` | 0 → 1 → 16 | 1 | 15 | True | True |
| Deffuant | CB− / global var. | `cb_minus_accept_ovar_gvar` | 0 → 4 → 4 | 4 | 0 | False | True |
| Deffuant | CB+ / global var. | `cb_plus_accept_ostd_gvar` | 0 → 2 → 2 | 2 | 0 | False | False |

The right-panel segment start/end coordinates, Micro reference onset and unchanged adjacent delays are recorded in source_data/figure_5_plotted_delays.tsv.

Full frozen indicator semantic names and node IDs are recorded in source_data/figure_5_supported_path_labels.tsv.

Inputs:
- `analysis/representative_path_selection.json`
- `analysis/path_intervention_classification.csv`
- `analysis/holdout_path_confirmation.csv`
- `analysis/path_timing_summary.csv`
- `analysis/effect_curves.parquet`
- `representation/indicators_frozen.json`
