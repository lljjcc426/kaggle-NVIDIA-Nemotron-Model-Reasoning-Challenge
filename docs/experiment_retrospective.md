# 实验路线复盘

## 有效信号

### 保守 adapter 包装

Mirza v16 和 Finding Nemo 都不是重训练路线。二者的共同点是依赖已经公开或可挂载的 adapter 产物，通过 Kaggle notebook 完成结构校验与 `submission.zip` 包装。最终私榜两个 `0.86` 都来自这一类。

结论：在提交次数受限、无法本地完整评测 30B 模型的条件下，保守 adapter 锚点比激进训练更可靠。

### 小幅结构保持校准

`localcal_rohan_anchor_lmhead_loraB_x1.01_structure_preserved` 取得公榜 `0.86`、私榜 `0.85`。这说明极小幅度、结构保持的 LoRA-B 缩放可能提升私榜稳健性，但缩放幅度扩大后并没有稳定收益。

### Biohack sparse-trust wrapper

`20260615_wrap_biohack_v62_public_sparse_trust_probe` 取得公榜 `0.86`、私榜 `0.85`，是改动型路线里最好的结果之一。该路线没有超过保守包装的私榜上限，但提供了比 Refine/RepairCal 更好的私榜迁移。

## 失效信号

### 公榜 0.86 plateau

本队公榜 `0.86` 提交中，绝大多数私榜回落到 `0.84` 或 `0.83`。公榜分数相同不代表隐藏测试另一半相同；在 0.86 plateau 内，提交间差异主要被四舍五入和测试半区分布掩盖。

### Refine QR-SVD

`20260615_refine_psf_clean_qrsvd_valid_probe` 的本地报告显示实际触发的是 QR-SVD rank-32 转换，不是 PSF 分支。它在公榜保持 `0.86`，私榜为 `0.84`。该结果说明干净的 rank-32 压缩能满足结构要求，但不能单独证明私榜泛化。

### RepairCal no-jitter

RepairCal 多个强度点在公榜维持 `0.86`，私榜集中在 `0.83-0.84`。该路线对公榜半区形成稳定 plateau，但没有转化为私榜优势。

### 大幅训练和公开高分复刻

多条 broad SFT、custom-CoT、task arithmetic、merge、公开高分直接复刻路线出现 `0.57`、`0.60-0.65`、`0.78-0.85` 等结果。主要问题包括 rank/结构不匹配、训练目标偏离、公开 notebook 依赖不可复现和对公榜半区过拟合。

## 方法层面的结论

1. 赛题的有效提交空间首先由 rank-32 LoRA 结构约束决定。结构正确是门槛，泛化仍取决于 adapter 本身。
2. 公榜半区不足以区分 0.86 plateau 内的真实质量。私榜揭示后，最强信号是已提交 artifact 的真实 privateScore。
3. 对隐藏集更稳的路线不是复杂度最高的路线，而是对原 adapter 能力破坏最小的路线。
4. 本队最后取得私榜 `0.86` 的关键提交来自 Mirza v16；另一个被公榜低估的 Finding Nemo 说明最终选择应保留至少一个早期保守锚点。
