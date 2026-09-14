Figure 11. Primary-to-holdout path confirmation. Panel a counts frozen candidates, saved path_temporally_qualified=True paths, saved path_classification=supported paths, and their saved holdout_confirmed=True paths, respectively. Counts are derived by exact scenario/path_id joins, with no reconstructed classification. Schelling: 16 → 15 → 3 → 2. Deffuant: 18 → 7 → 3 → 2. Panel b includes every Primary supported path and reports its saved path-level holdout classification. Holdout outcomes do not alter Primary classifications. Short labels affect text only; complete path IDs and exact statuses are in source_data/figure_11_confirmation_matrix.tsv. Tol and CB abbreviate tolerance and confidence bound; +/− indicate the saved intervention direction. No edge-level holdout conclusions are inferred. These are deterministic path counts, without averaging or uncertainty intervals.

Inputs:
- `representation/candidate_paths.json`
- `analysis/path_temporal_qualification.csv`
- `analysis/path_intervention_classification.csv`
- `analysis/holdout_path_confirmation.csv`
