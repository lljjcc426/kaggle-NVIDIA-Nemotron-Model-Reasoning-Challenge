# 实验路线复盘

这份复盘只使用封榜后已经揭示的分数、提交记录和本仓库保留的代码/metadata。核心问题不是“哪个公榜分数最高”，而是每一类调整在公榜和私榜上的实际迁移效果。

## 总体分数结构

最终提交快照中有 91 条 complete 且带私榜分数的记录。私榜最高分只有两条 `0.86`：

| Submission | Public | Private | 说明 |
| --- | ---: | ---: | --- |
| `20260605_slot4_mirzayasir_best_086_v16_remote_output` | 0.86 | 0.86 | Mirza v16 / adapter-v32 epoch5 包装路线 |
| `Notebook finding nemo | Version 1` | 0.84 | 0.86 | Finding Nemo 原始版，Kienngx/tinker 系 adapter 转换包装 |

公榜 `0.86` 的提交并不稳定。所有 public `0.86` 的 complete 提交在私榜上的分布为：

| Public | Private | Count |
| --- | ---: | ---: |
| 0.86 | 0.86 | 1 |
| 0.86 | 0.85 | 3 |
| 0.86 | 0.84 | 19 |
| 0.86 | 0.83 | 8 |

这说明公榜 `0.86` plateau 里大部分路线并没有真实泛化优势。赛前根据公榜内部排序选择 Mirza v16 是正确的，但把 Refine QR-SVD 作为第二槽的判断没有被私榜验证。

## 路线级汇总

路线聚类表保存在 `reports/route_retrospective_summary.csv`。核心结果如下：

| Route | Count | Public 0.86 | Private 0.86 | Private 0.85 | Best private |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mirza v16 / adapter-v32 epoch5 packaging | 1 | 1 | 1 | 0 | 0.86 |
| Finding Nemo original / Kienngx-tinker SVD packaging | 1 | 0 | 1 | 0 | 0.86 |
| Rohan/Kienngx small localcal scaling | 10 | 4 | 0 | 2 | 0.85 |
| Biohack sparse-trust | 2 | 2 | 0 | 1 | 0.85 |
| Huikang-Asalhi-Refine QR/SVD family | 6 | 3 | 0 | 2 | 0.85 |
| Symbolic-focused SFT | 3 | 1 | 0 | 1 | 0.85 |
| Kienngx RepairCal calibration | 6 | 6 | 0 | 0 | 0.84 |
| Merge/fusion/task arithmetic | 6 | 1 | 0 | 0 | 0.84 |
| Training/custom SFT attempts | 15 | 0 | 0 | 2 | 0.85 |

## 具体尝试、效果和判断

### 1. Mirza v16 adapter 包装

做了什么：

- 使用公开 notebook `Best 0.86 | NVIDIA Nemotron Notebook - Version 16`。
- 核心动作是挂载 `assiabenazzouz/adappter-v32-epoch-5`，把 `adapter_config.json` 和 `adapter_model.safetensors` 打包为 `submission.zip`。
- 没有重新训练、融合或改变 LoRA 结构。

效果：

- 提交 `20260605_slot4_mirzayasir_best_086_v16_remote_output` 公榜 `0.86`，私榜 `0.86`。
- 是本队唯一一条 public `0.86` 且 private 仍为 `0.86` 的提交。

判断：

- 该路线证明，在这个赛题里“保留强 adapter 原始能力”比临时训练和复杂融合更重要。
- notebook 本身很简单，分数来自底层 adapter，而不是包装代码。

### 2. Finding Nemo 原始版

做了什么：

- 提交 `finding nemo - Version 1`。
- metadata 显示其来源包括 `ryanholbrook/nvidia-nemotron-submission-demo`，模型输入包括 `kienngx/nemotron-nano-30b-trained/Triton/tinker-adapter/1`。
- notebook 中进行了 adapter 查找、配置修正、rank-32 约束下的 SVD/转换和最终 zip 包装。

效果：

- 提交 `Notebook finding nemo | Version 1` 公榜 `0.84`，私榜 `0.86`。
- 这是本队另一个私榜最高提交，也是最典型的“公榜低估、私榜上升”样本。
- 后续 `finding nemo 3adc97` 公榜 `0.86`，私榜 `0.84`；`Nemotron Verify Finding Nemo` 公榜 `0.85`，私榜 `0.84`。

判断：

- 原始 Finding Nemo 保留了对私榜半区更有利的 adapter 行为，后续版本虽然提高或维持了公榜，但损失了私榜迁移。
- 这条结果直接说明，公榜半区不是可靠的单一筛选器；最后选择时必须保留一个早期保守锚点。

### 3. Refine QR-SVD / Huikang-Asalhi-default20 系

做了什么：

- 围绕 Huikang/default20、Asalhi/default20 mirror、Refine f05d8a 和 `refine_psf_clean_qrsvd` 做 rank-32 转换、QR-SVD 压缩和清理。
- `20260615_refine_psf_clean_qrsvd_valid_probe` 的本地报告显示 PSF 分支没有触发，实际是 clean QR-SVD fused projection 转换。

效果：

- 该路线共 6 条 complete 记录，最高私榜 `0.85`。
- `20260615_refine_psf_clean_qrsvd_valid_probe` 公榜 `0.86`，私榜 `0.84`。
- `20260614_slot2_huikang_blocktopk_floor4_clean_probe` 公榜 `0.85`，私榜 `0.85`。

判断：

- QR-SVD/clean conversion 能保证结构合规，且公榜常能到 `0.86`，但没有带来私榜 `0.86`。
- block/top-k 这类更保守的清理在私榜没有明显劣化，但公榜低一点；整体仍低于 Mirza/Finding Nemo 两个最高提交。

### 4. Kienngx RepairCal

做了什么：

- 基于 Kienngx tinker adapter，对 LoRA-B tensor 做无 jitter 的小幅校准。
- 强度点覆盖 `0.0019`、`0.00195`、`0.001975`、`0.0020`、`0.0021` 和最终 `0.001925`。

效果：

- 6 条 RepairCal 提交全部公榜 `0.86`。
- 私榜没有一条达到 `0.85`，集中为 `0.83-0.84`。
- 最终 `20260615_repaircal_nojitter_s001925_center_fill_probe` 公榜 `0.86`，私榜 `0.84`。

判断：

- RepairCal 是公榜稳定器，不是私榜提升器。
- 这类小幅校准可能贴合了公榜半区，但没有改善另一半隐藏集。

### 5. Rohan/Kienngx small localcal scaling

做了什么：

- 对 Rohan/Kienngx anchor 做结构保持的小幅 LoRA-B 缩放。
- 尝试了 `x0.9975`、`x1.01`、`x1.02`、`x1.03`、`x1.04`、`x1.05`、`x1.15`、`x1.25` 等幅度。

效果：

- 10 条记录中 4 条公榜 `0.86`。
- 私榜最高 `0.85`，包括 `localcal_rohan_anchor_lmhead_loraB_x1.01_structure_preserved` 和 `x1.04`。
- 幅度继续放大后，私榜没有继续上升。

判断：

- 极小幅缩放能在不破坏结构的前提下带来一点私榜稳健性。
- 这个方向有信号，但上限没有超过保守 adapter 包装。

### 6. Biohack sparse-trust

做了什么：

- 复刻/包装 Biohack v62 sparse-trust finisher。
- 自己尝试了 `alpha=0.00085`，同时包装 public sparse-trust 输出。

效果：

- `20260615_wrap_biohack_v62_public_sparse_trust_probe` 公榜 `0.86`，私榜 `0.85`。
- `20260615_biohack_v62_alpha00085_sparse_trust_probe` 公榜 `0.86`，私榜 `0.83`。

判断：

- public sparse-trust 成品比本地 alpha 微调更稳。
- 这条路线属于有效改动型候选，但仍低于两个私榜 `0.86` 的保守包装路线。

### 7. Symbolic-focused SFT

做了什么：

- 根据题型结构做 symbolic-only 或 verified-focus 的轻量训练。
- 包括 `symbolic2 lr12`、`symbolic2 lr08_32`、`symbolic focused public`。

效果：

- 最好结果是 `symbolic2 lr12 v1 localcv825 symbolic-only validated`，公榜 `0.86`，私榜 `0.85`。
- 另外两条为私榜 `0.84`。

判断：

- 针对符号/规则题的轻量训练确实比大规模训练稳，但仍没有超过强 adapter 原始能力。
- 训练集六类题型接近平衡，过窄的题型强化难以覆盖隐藏集变化。

### 8. Merge、fusion、task arithmetic 和公开高分复刻

做了什么：

- 尝试 Rauffauzan fusion、Dedquoc SVD fusion、Dare merge、task arithmetic、公开 `0.87/0.88` adapter 复刻、Hammad/Kuang 等路线。

效果：

- merge/fusion/task arithmetic 6 条中只有 1 条公榜 `0.86`，最高私榜 `0.84`。
- public high-score copy attempts 6 条最高私榜 `0.85`，但没有任何一条公榜 `0.86`。
- 部分公开高分复刻出现 `0.60-0.65` 级别结果。

判断：

- 公开高分标题和原作者榜面分不能直接迁移到本队提交环境。
- adapter 来源、rank、命名、配置、压缩方式和 notebook 输出路径都可能改变结果。

### 9. Training/custom SFT

做了什么：

- 尝试 Muon/full SFT、Nemotron trained models、custom-CoT、S7 replay/seed stability 等训练型路线。

效果：

- 15 条训练/custom SFT 记录没有任何一条公榜或私榜达到 `0.86`。
- 代表性失败包括 `20260615_wrap_vaibhav_custom_cot_public_sft_probe`，公榜 `0.57`，私榜 `0.57`。
- 也有少数训练路线达到私榜 `0.85`，例如 `nemotron-s7-seed-stability-replay` 和 Muon full v5，但公榜只有 `0.84-0.85`。

判断：

- 在剩余时间短、提交次数少、缺少本地完整评测的条件下，训练型路线风险最高。
- 训练可能改善局部题型，但更容易破坏原 adapter 在隐藏题型上的通用能力。

## 最终方法判断

1. 结构合规只是门槛。rank-32、zip 根目录和 config 正确只能保证能评测，不能保证私榜泛化。
2. 公榜 `0.86` plateau 不能直接排序。队内 public `0.86` 里只有 1 条 private `0.86`。
3. 私榜最高两条都来自保守 adapter 路线。复杂融合、校准和训练没有超过原始强 adapter。
4. 第二槽的赛前判断应更重视“路线多样性和早期锚点”，而不是只看最后几天公榜 `0.86` 的相对排序。
5. 对这类 hidden split 比赛，最终选择需要同时保留一条当前公榜最强提交和一条被公榜低估但结构保守的提交。
