# Technical Postmortem

## Scope

本报告基于封榜后的本队提交记录、Kaggle leaderboard 快照、kernel metadata、关键路线脚本和本地 artifact report。重点分析四个问题：

1. 分数真实分布是什么。
2. 我们做过哪些模型/adapter 调整。
3. 每类调整在 public/private split 上产生了什么效果。
4. 哪些判断被私榜验证，哪些判断失效。

## Evidence

| Evidence | File |
| --- | --- |
| Final submissions with private scores | `reports/submissions_final_2026-06-16_page200.csv` |
| Private leaderboard snapshot | `reports/private_leaderboard_show_2026-06-16_page200.csv` |
| Public leaderboard snapshot | `reports/public_leaderboard_download_2026-06-16.csv` |
| Public-to-private transition matrix | `reports/public_private_transition_matrix.csv` |
| Route-level statistics | `reports/route_detailed_statistics.csv` |
| Stage-level statistics | `reports/stage_score_summary.csv` |
| Key candidate review | `reports/key_candidate_review.csv` |
| Model artifact manifest | `reports/model_artifact_manifest.csv` |

## Competition Mechanics

The competition evaluates a rank-32-or-lower LoRA adapter on NVIDIA Nemotron-3-Nano-30B-A3B-BF16. The scoring side loads `adapter_config.json` and `adapter_model.safetensors`, runs deterministic vLLM inference, extracts the final answer from `\boxed{}`, and scores exact or tolerance-based correctness.

The train set contains 9500 rows and is close to balanced across six task families:

| Family | Count |
| --- | ---: |
| bit manipulation | 1602 |
| gravity | 1597 |
| unit conversion | 1594 |
| cipher | 1576 |
| numeral system | 1576 |
| equation | 1555 |

This distribution made narrow family specialization risky. A route could improve one family and still lose private performance if it damaged other reasoning modes.

## Final Result

| Metric | Value |
| --- | --- |
| Team | 你跑不过我你信吗 |
| TeamId | 15826879 |
| Final private score | 0.86 |
| Final private rank | 121 |
| Public score | 0.86 |
| Public rank | 422 |
| Submission count | 132 |

The team moved from public rank 422 to final/private rank 121 at the same displayed score `0.86`. This is consistent with the private split rewarding a different subset of routes than the public split.

## Score Distribution

Among 91 complete submissions with private scores:

| Private score | Count |
| --- | ---: |
| 0.86 | 2 |
| 0.85 | 10 |
| 0.84 | 45 |
| 0.83 | 15 |
| <= 0.82 | 19 |

The public `0.86` group was highly heterogeneous:

| Public | Private | Count |
| --- | ---: | ---: |
| 0.86 | 0.86 | 1 |
| 0.86 | 0.85 | 3 |
| 0.86 | 0.84 | 19 |
| 0.86 | 0.83 | 8 |

Only one public `0.86` submission remained private `0.86`: `20260605_slot4_mirzayasir_best_086_v16_remote_output`.

## Best Private Submissions

| Submission | Public | Private | Interpretation |
| --- | ---: | ---: | --- |
| `Notebook finding nemo | Version 1` | 0.84 | 0.86 | Public underestimated a conservative Kienngx/tinker-derived adapter route. |
| `20260605_slot4_mirzayasir_best_086_v16_remote_output` | 0.86 | 0.86 | Best public-aligned route and the only public-0.86 submission that held private 0.86. |

These two submissions define the post-competition lesson: the best final pair should combine a current public-strong adapter with an earlier conservative anchor that may be under-ranked by public split.

## Route Analysis

### Conservative Adapter Packaging

What changed:

- Mirza v16 packaged `assiabenazzouz/adappter-v32-epoch-5`.
- Finding Nemo original used the Kienngx/tinker adapter source and performed adapter discovery, config correction, rank-32 SVD/conversion, and packaging.

Observed effect:

- Mirza v16: public `0.86`, private `0.86`.
- Finding Nemo original: public `0.84`, private `0.86`.
- Later Finding Nemo variants did not preserve the private behavior: `finding nemo 3adc97` was public `0.86`, private `0.84`.

Judgment:

- The strongest hidden performance came from preserving strong adapter behavior, not from adding more transformations.
- The original Finding Nemo result shows that public LB can under-rank a private-robust adapter.

### QR-SVD / Refine / Huikang-Asalhi Family

What changed:

- Converted or compressed Huikang/default20 and Asalhi/default20-derived adapters into rank-32-compatible submissions.
- The final Refine PSF Clean route was effectively QR-SVD fused-projection conversion; PSF did not trigger in the report.

Observed effect:

- 6 complete submissions.
- 3 public `0.86`.
- Best private `0.85`.
- Final Refine candidate: public `0.86`, private `0.84`.

Judgment:

- QR-SVD conversion solved structural compatibility but did not create private robustness.
- This route looked strong during final public ranking but did not transfer to the private split.

### RepairCal Calibration

What changed:

- Applied no-jitter LoRA-B scaling to Kienngx/tinker adapter.
- Tested strengths around `0.0019-0.0021`; final center point was `0.001925`.

Observed effect:

- 6 complete RepairCal submissions.
- All 6 reached public `0.86`.
- None reached private `0.85`; results concentrated at private `0.83-0.84`.

Judgment:

- RepairCal was a public plateau stabilizer.
- The calibration likely fit public split behavior and failed to improve the private split.

### Small Localcal Scaling

What changed:

- Applied small structure-preserving LoRA-B scaling to Rohan/Kienngx anchor variants.
- Explored values around `x0.9975` to `x1.25`.

Observed effect:

- 10 submissions.
- 4 public `0.86`.
- Best private `0.85`, notably `x1.01` and `x1.04`.

Judgment:

- Tiny scale changes can improve robustness without severe breakage.
- The signal was real but capped below the conservative adapter top two.

### Biohack Sparse-Trust

What changed:

- Tested public Biohack v62 sparse-trust output and a local `alpha=0.00085` variant.

Observed effect:

- Public wrapper: public `0.86`, private `0.85`.
- Local alpha variant: public `0.86`, private `0.83`.

Judgment:

- Sparse-trust was the best modified route outside the two private-0.86 submissions.
- The public artifact was more reliable than the local alpha tweak.

### Symbolic-Focused SFT

What changed:

- Focused training on symbolic/verified subsets with low learning-rate variants.

Observed effect:

- 3 complete submissions.
- Best result: public `0.86`, private `0.85`.

Judgment:

- Light symbolic tuning was safer than broad training.
- It did not exceed the original adapter routes because the hidden test remained multi-family.

### Merge, Fusion, Task Arithmetic, And Public High-Score Copies

What changed:

- Tried adapter fusion, DARE merge, task arithmetic, and public high-score copies such as Hammad/Kuang/Dedquoc-style routes.

Observed effect:

- Merge/fusion/task arithmetic: 6 submissions, best private `0.84`.
- Public high-score copy attempts: 6 submissions, best private `0.85`, with several much lower outcomes.

Judgment:

- Public notebook titles and claimed scores did not transfer reliably.
- Adapter source, rank conversion, target module naming, and Kaggle input layout were enough to change outcomes materially.

### Training / Custom SFT

What changed:

- Tested Muon/full SFT, trained model submissions, custom-CoT wrappers, S7 replay/seed-stability variants.

Observed effect:

- 15 complete submissions.
- No public or private `0.86`.
- A representative failure was `20260615_wrap_vaibhav_custom_cot_public_sft_probe`: public `0.57`, private `0.57`.

Judgment:

- Full training and custom-CoT were too high-risk under the time and evaluation constraints.
- They often damaged broad hidden-task behavior even when some local or public signal looked plausible.

## Stage-Level Read

| Stage | What happened | Result |
| --- | --- | --- |
| Early anchors and symbolic probes | Submitted original Finding Nemo and symbolic variants | Produced one private `0.86` and several private `0.85` results |
| Public-source exploration and adapter packaging | Tested Mirza, Taha, Mohamed, Rauffauzan, Hammad/Kuang copies | Mirza produced the only public-0.86/private-0.86 result |
| Local calibration and training probes | Explored localcal, public 0.87 copies, Muon/S7 variants | Localcal gave private `0.85`; broad training was unstable |
| Merge/refine/training expansion | Tried merge and refine routes | Most results stayed `0.83-0.84` private |
| Final sprint | RepairCal, Refine, Biohack, wrappers | Biohack wrapper reached private `0.85`; Refine/RepairCal were public-stable but private `0.84` |

## Final Selection Error

The final pre-private analysis correctly identified Mirza v16 as the strongest first slot. The error was selecting Refine QR-SVD over the early Finding Nemo original.

Why the error happened:

- Refine had stronger late public ordering and cleaner local audit reports.
- RepairCal/Refine appeared route-stable because many variants produced public `0.86`.
- Finding Nemo original looked weaker on public score at `0.84`.

Why private results contradicted that:

- Public stability in the `0.86` plateau did not imply private robustness.
- The original Finding Nemo route preserved a useful behavior that later transformations and final-sprint calibrations weakened.
- Auditability and structural cleanliness were useful engineering properties, but not direct scoring predictors.

## Model Artifact Policy

The repository now allows model/adapter weight formats through Git LFS via `.gitattributes`. `submission.zip` remains ignored because it is an evaluation package, not the model artifact itself.

The model artifact manifest is `reports/model_artifact_manifest.csv`. It separates:

- external Kaggle model/dataset sources,
- locally generated adapter reports,
- weight sizes,
- SHA256 where available,
- score linkage,
- whether the raw weight is stored.

This keeps the repository reviewable while still leaving a clean path for publishing actual adapter weights through Git LFS or GitHub Releases.

## Lessons

1. Do not rank final submissions solely by public `0.86`.
2. Keep at least one conservative early adapter anchor if public/private split is large.
3. Treat repeated public plateau hits as evidence of validity, not evidence of private lift.
4. Prefer transformations that preserve adapter behavior unless a controlled private-like validation signal exists.
5. Track model artifact provenance separately from `submission.zip`.
6. When local full-model validation is impossible, submission portfolio diversity matters more than late public score polishing.
