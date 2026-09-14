Figure 6. Standardised paired cumulative effects for Schelling (a) and Deffuant (b). Rows denote saved parameter-direction conditions; columns are grouped into Micro, Meso and Macro. Mi, Me and Ma codes number indicators in node-ID order within each scale and scenario; the full frozen semantic-name mapping is supplied in source_data/figure_6_indicator_codebook.tsv. Both panels share the original diverging palette and one colourbar centred on zero. The limits are [−13.5952037964, +13.5952037964], calculated from the maximum absolute finite cumulative_effect_standardised across both scenarios, without percentile clipping or saturation of any defined point estimate. Dots preserve the saved significant flags, all of which satisfy 95% CI exclusion of zero as well as the run's original additional significance criteria. These flags are not recomputed from interval signs alone. In this figure, slash-marked cells indicate undefined standardized effects because baseline variance is zero. Undefined cells use the same neutral colour as zero, with a small, light-grey / in the upper-right corner; their data remain NaN and they receive no significance dot. No paired effects, confidence intervals, significance decisions or experimental settings are altered.

The full plotted cells and their saved values are supplied in source_data/figure_6_plotted_cells.tsv.

Inputs:
- `analysis/paired_effects.parquet`
- `representation/indicators_frozen.json`
- `config/experiment_config.snapshot.json`
