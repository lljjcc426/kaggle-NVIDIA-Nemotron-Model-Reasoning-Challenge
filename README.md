# NVIDIA Nemotron Model Reasoning Challenge 复盘

本仓库整理 NVIDIA Nemotron Model Reasoning Challenge 的队伍实验记录、最终榜单快照、提交分数和关键代码路线。重点是封榜后的私榜验证，而不是公榜 0.86 段内的表面排序。

## 最终结果

| 项目 | 结果 |
| --- | --- |
| 队伍 | 你跑不过我你信吗 |
| TeamId | 15826879 |
| 最终私榜分数 | 0.86 |
| 最终私榜排名 | 121 |
| 公榜分数 | 0.86 |
| 公榜排名 | 422 |
| 提交次数 | 132 |

最终私榜排名来自 `kaggle competitions leaderboard --show --csv --page-size 200` 的分页快照；公榜排名来自 Kaggle 下载的 `publicleaderboard` 文件。两份快照分别保存在 `reports/` 中。

## 关键结论

- 公榜 `0.86` 不是充分信号。本队公榜 `0.86` 的提交中，私榜只有 1 条保持 `0.86`，3 条为 `0.85`，19 条为 `0.84`，8 条为 `0.83`。
- 私榜最高两个提交是 [`finding nemo - Version 1`](https://www.kaggle.com/code/llccqq624/finding-nemo?scriptVersionId=322459680) 和 [`Best 0.86 | NVIDIA Nemotron Notebook - Version 16`](https://www.kaggle.com/code/mirzayasirabdullah07/nvidia-nemotron-notebook-final-code?scriptVersionId=324524084)。
- `20260605_slot4_mirzayasir_best_086_v16_remote_output` 公榜 `0.86`，私榜 `0.86`，是唯一一条 public `0.86` 且 private 保持 `0.86` 的队内提交。
- `Notebook finding nemo | Version 1` 公榜只有 `0.84`，私榜达到 `0.86`，说明另一半隐藏测试对保守 Kienngx/tinker 系 adapter 更友好。
- `Refine QR-SVD`、`RepairCal`、`Asalhi/default20` 等公榜稳定 `0.86` 路线在私榜集中回落到 `0.84`，说明对公榜半区的微调校准没有可靠迁移。
- `Biohack v62 public sparse-trust wrapper` 是少数公榜 `0.86`、私榜 `0.85` 的改动型路线，但仍未超过两个私榜 `0.86` 提交。
- 大规模自训练、merge/task arithmetic、未经验证的公开高分复刻和 custom-CoT 路线在本队提交记录中多次表现为 `0.83` 以下或结构性失败。

## 仓库结构

| 路径 | 内容 |
| --- | --- |
| `docs/competition_and_metric.md` | 赛题约束、数据分布、评分机制 |
| `docs/final_results.md` | 私榜/公榜快照与提交结果 |
| `docs/technical_postmortem.md` | 更完整的技术复盘：证据、路线、阶段、误差和模型 artifact |
| `docs/experiment_retrospective.md` | 按调整路线展开的“做了什么、效果、判断”复盘 |
| `docs/model_artifacts.md` | 模型/adapter 发布策略和 artifact manifest |
| `docs/artifact_inventory.md` | 本仓库收录与排除规则 |
| `reports/` | Kaggle CLI 快照和派生统计表 |
| `src/` | 关键 adapter 包装、压缩、校验脚本 |
| `metadata/` | 关键 Kaggle kernel metadata |

## 文件取舍

仓库不包含 `submission.zip`、`adapter_model.safetensors`、Kaggle 缓存、临时拉取目录、训练中间产物和大体积本地输出。相关文件通常为 3GB 级别，且 GitHub 不适合承载这类二进制产物。可审计信息通过 Kaggle kernel metadata、提交记录、榜单快照、脚本和复盘表保留。

## 数据快照

- `reports/submissions_final_2026-06-16_page200.csv`: Kaggle CLI 拉取的最终提交记录，98 条记录，91 条 complete 且有私榜分数。
- `reports/private_leaderboard_show_2026-06-16_page200.csv`: 封榜后 `leaderboard --show` 分页快照，队伍在该快照中排名 121。
- `reports/public_leaderboard_download_2026-06-16.csv`: Kaggle 下载的 public leaderboard，队伍公榜排名 422。
- `reports/train_family_distribution.csv`: 训练集 9500 条样本的任务族统计。
- `reports/route_retrospective_summary.csv`: 各实验路线的提交数、公榜/私榜分布和最高私榜结果。
- `reports/route_detailed_statistics.csv`: 路线级均值、中位数、private-public delta 和最佳提交。
- `reports/public_private_transition_matrix.csv`: public score 到 private score 的转移矩阵。
- `reports/stage_score_summary.csv`: 不同实验阶段的分数汇总。
- `reports/key_candidate_review.csv`: 最关键候选提交的逐条判读。
- `reports/model_artifact_manifest.csv`: 模型/adapter 来源、大小、hash 和分数关联。

## 核心代码

- `src/package_mirza_v16_adapter.py`: Mirza v16 adapter-v32-epoch-5 包装脚本。
- `src/package_finding_nemo_rank32_svd.py`: Finding Nemo/Kienngx 系 rank-32 SVD adapter 转换脚本。
- `src/package_huikang_refine_psf_clean.py`: Huikang/default20 QR-SVD Refine 路线。
- `src/package_kienngx_repaircal_nojitter_strength001925.py`: Kienngx RepairCal no-jitter 路线。
- `src/wrap_biohack_v62_public.py`: Biohack v62 public sparse-trust wrapper。
