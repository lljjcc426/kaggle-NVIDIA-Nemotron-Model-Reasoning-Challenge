# NVIDIA Nemotron Model Reasoning Challenge

本仓库是 NVIDIA Nemotron Model Reasoning Challenge 的赛后技术复盘与 artifact 索引，整理内容包括最终公榜/私榜结果、全部可取得提交的逐条复盘、实验路线分析、模型/adapter 来源、关键脚本和 Kaggle metadata。

复盘目标是回答三个问题：

1. 哪些操作真实提升或保持了私榜表现。
2. 哪些公榜 `0.86` 只是 public split plateau，没有迁移到 private split。
3. 在无法本地完整评测 30B 模型的条件下，哪些提交选择策略更可靠。

## Final Result

| Item | Value |
| --- | --- |
| Team | 你跑不过我你信吗 |
| TeamId | 15826879 |
| Final private score | 0.86 |
| Final private rank | 121 |
| Public score | 0.86 |
| Public rank | 422 |
| Kaggle leaderboard submission count | 132 |

私榜排名来自 `kaggle competitions leaderboard --show --csv --page-size 200` 的封榜后快照；公榜排名来自 Kaggle 下载的 `publicleaderboard` 文件。对应原始文件保存在 `reports/`。

## Best Private Submissions

| Submission | Public | Private | Route |
| --- | ---: | ---: | --- |
| [`finding nemo - Version 1`](https://www.kaggle.com/code/llccqq624/finding-nemo?scriptVersionId=322459680) | 0.84 | 0.86 | Original Finding Nemo / Kienngx-tinker adapter conversion |
| [`Best 0.86 | NVIDIA Nemotron Notebook - Version 16`](https://www.kaggle.com/code/mirzayasirabdullah07/nvidia-nemotron-notebook-final-code?scriptVersionId=324524084) | 0.86 | 0.86 | Mirza v16 / adapter-v32 epoch5 packaging |

这两条定义了最终复盘的核心结论：私榜最稳的不是最后几天反复贴合公榜 `0.86` 的校准路线，而是对强 adapter 行为破坏最小的保守包装/转换路线。

## Key Findings

- 公榜 `0.86` 不是充分信号。最终 complete 且有私榜分数的提交中，public `0.86` 的结果分化为：private `0.86` 1 条、`0.85` 3 条、`0.84` 19 条、`0.83` 8 条。
- Mirza v16 是唯一一条 public `0.86` 且 private 保持 `0.86` 的队内提交。
- Finding Nemo 原始版 public `0.84`、private `0.86`，说明 public split 低估了一个私榜稳健的早期 adapter 锚点。
- RepairCal 产生 6 条 public `0.86`，但 private 全部低于 `0.85`，属于公榜稳定器，不是私榜提升器。
- Refine QR-SVD / Huikang-Asalhi-default20 系能保持结构合规，也能多次达到 public `0.86`，但最终没有产生 private `0.86`。
- Biohack sparse-trust public wrapper 是最好的改动型路线之一，public `0.86`、private `0.85`，仍低于两个 private `0.86` 的保守路线。
- Training/custom SFT、merge/fusion/task arithmetic、公开高分复刻在本队提交中整体风险更高，多个方向出现 private `0.83` 以下或评测失败。

## Evidence Snapshot

| Evidence | File |
| --- | --- |
| Final submissions with private scores | `reports/submissions_final_2026-06-16_page200.csv` |
| Per-submission operation review | `reports/all_submission_operation_ledger.csv` |
| Rendered all-submission ledger | `docs/all_submissions_operation_ledger.md` |
| Public-to-private transition matrix | `reports/public_private_transition_matrix.csv` |
| Route-level detailed statistics | `reports/route_detailed_statistics.csv` |
| Stage-level score summary | `reports/stage_score_summary.csv` |
| Key candidate review | `reports/key_candidate_review.csv` |
| Model / adapter artifact manifest | `reports/model_artifact_manifest.csv` |

Kaggle CLI 当前可返回的最终提交记录为 98 条，其中 91 条 complete 且带 privateScore，6 条为 evaluation error。赛前本地快照保留过 138 条记录，但该快照没有 privateScore，因此公私榜对照复盘以封榜后 98 条最终记录为准。

## Repository Structure

| Path | Purpose |
| --- | --- |
| `docs/technical_postmortem.md` | 全面技术复盘：证据、赛题机制、路线、阶段、错误判断和 artifact 策略 |
| `docs/experiment_retrospective.md` | 按实验路线展开的“做了什么、效果、判断”复盘 |
| `docs/all_submissions_operation_ledger.md` | 每条提交的操作类别、公榜、私榜、delta 和结果判读 |
| `docs/final_results.md` | 最终榜单位置、分数分布和最高提交 |
| `docs/competition_and_metric.md` | 赛题约束、评分机制和训练集题型分布 |
| `docs/model_artifacts.md` | 模型/adapter 发布策略，区分权重、config 和 `submission.zip` |
| `docs/artifact_inventory.md` | 仓库收录、排除和来源清单 |
| `reports/` | 原始 Kaggle 快照和派生统计表 |
| `src/` | 关键 adapter 包装、rank-32 SVD、Refine、RepairCal、Biohack wrapper 脚本 |
| `metadata/` | 关键 Kaggle kernel metadata |

## Operation Review

所有最终可取得提交都已按操作类别复盘：

| Operation category | Main result |
| --- | --- |
| Adapter packaging | Mirza v16 保持 public/private `0.86/0.86` |
| Rank-32 SVD adapter packaging | Finding Nemo 原始版从 public `0.84` 提升到 private `0.86` |
| RepairCal calibration | 多次 public `0.86`，private 集中在 `0.83-0.84` |
| Localcal LoRA-B scaling | 小幅缩放可到 private `0.85`，但没有突破 `0.86` |
| QR-SVD / adapter cleanup | 结构合规，最高 private `0.85` |
| Sparse-trust wrapper | Biohack public wrapper 达到 private `0.85` |
| Symbolic-focused SFT | 轻量训练最高 private `0.85` |
| Merge/fusion/task arithmetic | 未产生 private `0.86`，多条回落 |
| Training/custom SFT | 失败和弱迁移最多，没有 private `0.86` |
| Public high-score reproduction | 公开高分标题无法直接迁移到本队提交环境 |

逐条明细见 `docs/all_submissions_operation_ledger.md`。

## Model And Adapter Artifacts

本仓库允许发布模型/adapter 相关材料，但不发布 Kaggle `submission.zip`。`submission.zip` 是评测提交包，不是模型 artifact 本体。

当前策略：

- `adapter_config.json` 等小文件可以直接进入普通 Git。
- `.safetensors`、`.bin`、`.pt`、`.pth`、`.ckpt` 已通过 `.gitattributes` 配置为 Git LFS。
- `*.zip` 继续在 `.gitignore` 中排除，避免误传 Kaggle submission 包。
- 模型/adapter 来源、大小、hash 和分数关联统一记录在 `reports/model_artifact_manifest.csv`。

## Key Code

| Script | Route |
| --- | --- |
| `src/package_mirza_v16_adapter.py` | Mirza v16 adapter-v32 epoch5 packaging |
| `src/package_finding_nemo_rank32_svd.py` | Finding Nemo / Kienngx rank-32 SVD adapter conversion |
| `src/package_huikang_refine_psf_clean.py` | Huikang/default20 Refine QR-SVD route |
| `src/package_kienngx_repaircal_nojitter_strength001925.py` | Kienngx RepairCal no-jitter calibration |
| `src/wrap_biohack_v62_public.py` | Biohack v62 public sparse-trust wrapper |

## Bottom Line

最终私榜验证表明，最有价值的策略不是继续微调 public `0.86` plateau，而是保留强 adapter 的原始泛化能力，并用不同来源的保守锚点覆盖 public/private split 差异。Mirza v16 证明了当前公榜强信号的价值；Finding Nemo 原始版证明了被公榜低估的早期 conservative adapter 在私榜上可能更稳。
