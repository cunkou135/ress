# Figure 9–12 绘图交付报告

数据源：`E:\work\毕业论文相关\数据驱动方法\(ACL 2026)CAMO\小论文\91exp\_code\runs\baoba20260904_01`

输出目录：`E:\work\毕业论文相关\数据驱动方法\(ACL 2026)CAMO\小论文\91exp\_code\paper_fig`

四张图均使用现有 Python/Matplotlib 绘图方式，沿用 Schelling 蓝色 `#2B5D7E`、Deffuant 红色 `#B84A3C`、浅色背景、Arial 字体及简洁坐标轴。PNG 为 300 dpi；SVG 保留可编辑文字。仅新增 Figure 9–12 绘图代码、图片及其来源/核验附件。

## Figure 9：方法组件消融

- 文件：`analysis/functional_ablations.csv`。
- 字段：`scenario`、`variant`、`evaluation_track`、`stability`、`intervention_support_rate`、`mean_ci_width`。
- 按请求绘制 `full_method`、`without_joint_trajectories`、`without_bootstrap`、`without_structured_representation`、`without_paired_seeds`。源文件共 12 条汇总记录；所选 5 个 variant × 2 个场景共 10 条。
- a/b/c 分别绘制 Stability、Intervention support rate、Mean CI width。直接使用已有汇总值，不重新求均值，也不添加无来源区间。类别之间不连成连续曲线。
- a 有 6 个有效值和 4 个 NaN：两个场景的 `without_joint_trajectories`、`without_bootstrap` stability 均缺失，保留空白。b/c 各有 10 个有效值。
- 代码：`draw_figure_9_functional_ablations.py`。
- 输出：`figure_9_functional_ablations.png`、`figure_9_functional_ablations.svg`。

## Figure 10：Stage 1 表征错误鲁棒性

- 文件：`analysis/representation_robustness.csv`。
- 字段：`scenario`、`operator`、`error_ratio`、`repetition`、`evaluation_track`、`candidate_edge_count`、`retained_edge_count`、`temporal_qualification_rate`、`stability`。
- 2 × 5 面板，列顺序为 `irrelevant_indicator`、`redundant_semantic_indicator`、`delete_candidate_relation`、`wrong_hypothesis_group_assignment`、`cross_hypothesis_group_relation`；上行为 qualification rate，下行为 stability。
- 共 480 条重复记录：2 场景 × 5 operators × 4 error ratios（0、0.1、0.2、0.4）× 12 repetitions；40 个条件、80 个指标汇总点。两项指标均无缺失。
- 每个 scenario × operator × error_ratio 内，中心线为 12 次重复的 median，阴影为 25th–75th percentile（IQR，线性分位数插值）。IQR 表示重复实验变异，不是 confidence interval。
- qualification rate 直接读 CSV，并核对其等于 retained candidate relations / total candidate relations。不计算或使用 F1。
- 代码：`draw_figure_10_representation_robustness.py`。
- 输出：`figure_10_representation_robustness.png`、`figure_10_representation_robustness.svg`。

## Figure 11：Primary → Holdout confirmation

- 文件：`representation/candidate_paths.json`、`analysis/path_temporal_qualification.csv`、`analysis/path_intervention_classification.csv`、`analysis/holdout_path_confirmation.csv`。
- 关键字段：candidate JSON 的 `scenarios`、`path_id`；Stage 2 的 `scenario`、`path_id`、`path_temporally_qualified`；Stage 3 的 `path_classification`；Holdout 的 `classification`、`holdout_confirmed`。另外核对 `parameter`、`direction`、`micro`、`meso`、`macro`、`evaluation_track`、`primary_result_unchanged` 及冻结路径身份。
- a 根据 scenario/path_id 的真实集合计数：Candidate → Temporal-qualified → Primary-supported → Holdout-confirmed。

| 场景 | Candidate | Temporal-qualified | Primary-supported | Holdout-confirmed |
|---|---:|---:|---:|---:|
| Schelling | 16 | 15 | 3 | 2 |
| Deffuant | 18 | 7 | 3 | 2 |

- b 包含全部 6 条 Primary supported paths：4 条 Holdout confirmed，2 条 Holdout inconclusive。路径依照 path_id 确定性排序，短标签仅改变显示文字，完整 ID 保存在来源表。
- 不重新判定分类，不推导 edge-level holdout 结论；没有平均或区间估计。
- 代码：`draw_figure_11_holdout_confirmation.py`。
- 输出：`figure_11_holdout_confirmation.png`、`figure_11_holdout_confirmation.svg`。

## Figure 12：Observational timing vs intervention timing

- 主文件：`analysis/path_timing_concordance.csv`；辅助读取 `analysis/path_temporal_qualification.csv`，仅用于验证 Stage 2 入选路径集合。
- 分组/筛选字段：`scenario`、`path_id`、`path_classification`、`path_temporally_qualified`。

| 面板 | x 字段 | y 字段 | 有效坐标对 | 缺失坐标对 |
|---|---|---|---:|---:|
| a Micro→Meso | `micro_meso_observational_lag` | `micro_meso_intervention_delay` | 14 | 8 |
| b Meso→Macro | `meso_macro_observational_lag` | `meso_macro_intervention_delay` | 14 | 8 |
| c Total timing | `observational_total_lag` | `intervention_total_latency` | 16 | 6 |

- 实际保存的总观测时延字段名为 `observational_total_lag`，并非请求示例中的 `total_observational_lag`；直接使用真实列，不补算总时延。
- 入选 22 条路径：Schelling 15、Deffuant 7。a/b 的有效坐标对分别来自 Schelling 10、Deffuant 4；c 为 Schelling 12、Deffuant 4。所有路径均保存在来源表；缺失坐标不填数。
- 直接散点，无平均或坐标抖动。颜色区分场景，形状区分 supported / contradicted / inconclusive / manipulation_failure。相同坐标仍逐条绘制，并在需要时用小计数标记解释重叠。
- 三个面板均保留全部 6 条 supported paths，包括观测 lag 与干预 delay 不一致者。b 中 3 个负 delay 亦原样保留。y=x 仅为参考线，不参与分类或筛选。
- 代码：`draw_figure_12_timing_concordance.py`。
- 输出：`figure_12_timing_concordance.png`、`figure_12_timing_concordance.svg`。

## 附件与核验

- 新增共用 helper：`figure_9_12_helpers.py`，仅供这四张新图使用。
- 每图 caption：`figure_9_caption.md` 至 `figure_12_caption.md`；绘图来源表在本目录的 `source_data` 子目录。
- 每图核验记录：本目录 `qa/figure_9_verification.json` 至 `qa/figure_12_verification.json`。
- Figure 9 的 30 个指标记录、Figure 10 的 80 个 median/IQR 汇总、Figure 11 的路径计数和 6 行矩阵、Figure 12 的 66 个坐标记录均已与原始文件逐项核对。SVG 中的 Figure 10 曲线/阴影坐标和 Figure 12 有效点坐标亦已核对。四张 PNG 已完成视觉检查。
- 修改前后 241 个受保护现有文件 SHA256 一致；正式 run 的 3,805 个文件清单、大小及修改时间一致。Figure 2–8、实验代码、科学结果、方法、阈值、种子与分类逻辑未修改，未重新运行实验。
- 重绘时分别执行相应 `draw_figure_*.py`，脚本默认从正式 run 读取并输出到本目录；支持 `--run`、`--output-dir` 参数。当前使用 `E:\conda\python.exe -B` 执行。
