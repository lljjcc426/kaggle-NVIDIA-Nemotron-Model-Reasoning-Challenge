# 最终结果与提交分析

## 榜单位置

| 快照 | Rank | Score | Rows | 文件 |
| --- | ---: | ---: | ---: | --- |
| final/private `leaderboard --show` | 121 | 0.86 | 906 | `reports/private_leaderboard_show_2026-06-16_page200.csv` |
| public leaderboard download | 422 | 0.86 | 4355 | `reports/public_leaderboard_download_2026-06-16.csv` |

队伍 `TeamId=15826879`，队伍名 `你跑不过我你信吗`。封榜后最终分数为 `0.86`，最终排名以 `leaderboard --show` 的私榜快照为准。

## 提交记录

最终提交快照 `reports/submissions_final_2026-06-16_page200.csv` 包含 98 条记录，其中 91 条为 complete 且带有私榜分数。

私榜分布：

| Private score | Count |
| --- | ---: |
| 0.86 | 2 |
| 0.85 | 10 |
| 0.84 | 45 |
| 0.83 | 15 |
| 0.82 | 2 |
| 0.79 | 1 |
| 0.76 | 2 |
| 0.72 | 2 |
| 0.71 | 2 |
| 0.70 | 1 |
| 0.69 | 1 |
| 0.65 | 4 |
| 0.64 | 1 |
| 0.57 | 1 |
| 0.55 | 1 |
| 0.24 | 1 |

公榜 `0.86` 的提交在私榜上的分化：

| Public | Private | Count |
| --- | --- | ---: |
| 0.86 | 0.86 | 1 |
| 0.86 | 0.85 | 3 |
| 0.86 | 0.84 | 19 |
| 0.86 | 0.83 | 8 |

## 私榜最佳提交

| Date | Description | Public | Private | 判读 |
| --- | --- | ---: | ---: | --- |
| 2026-06-05 06:58:51 | `20260605_slot4_mirzayasir_best_086_v16_remote_output` | 0.86 | 0.86 | 最终核心提交，赛前队内公榜最高，私榜保持 0.86 |
| 2026-05-27 07:44:45 | `Notebook finding nemo | Version 1` | 0.84 | 0.86 | 公榜低估、私榜上升，保守 Kienngx/tinker 系路线 |
| 2026-05-27 13:49:06 | `symbolic2 lr12 v1 localcv825 symbolic-only validated` | 0.86 | 0.85 | 符号类轻量路线，私榜较稳但未到 0.86 |
| 2026-06-06 08:05:41 | `localcal_rohan_anchor_lmhead_loraB_x1.01_structure_preserved` | 0.86 | 0.85 | 小幅结构保持校准，私榜优于多数 0.86 |
| 2026-06-15 04:32:34 | `20260615_wrap_biohack_v62_public_sparse_trust_probe` | 0.86 | 0.85 | 改动型路线中私榜表现最好 |

## 最终选择复盘

赛前根据队内公榜排序选择 Mirza v16 是有效的；该提交最终保持私榜 `0.86`。第二选择 Refine QR-SVD 的判断没有被私榜验证，`20260615_refine_psf_clean_qrsvd_valid_probe` 最终为公榜 `0.86`、私榜 `0.84`。

最关键的误差来自把公榜 `0.86` 内部排序和路线稳定性当成私榜迁移信号。封榜后数据表明，公榜半区中后段的 adapter 微调、rank 压缩和轻量校准并不必然迁移到私榜半区。`Finding Nemo` 的反向表现说明另一半隐藏集对早期保守 adapter 锚点更友好。
