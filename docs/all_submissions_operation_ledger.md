# All Submissions Operation Ledger

Generated from `reports/submissions_final_2026-06-16_page200.csv`. This ledger reviews every final Kaggle submission returned by the CLI with public/private score, operation type, and observed result.

Final available rows: `98`; complete rows: `91`; error rows: `6`. The pre-final historical snapshot had `138` rows but did not include private scores, so score-based public/private review uses the final 98-row snapshot.

## Outcome Counts

| Outcome | Count |
| --- | ---: |
| `middle_stable` | 26 |
| `public_plateau_drop` | 19 |
| `weak_transfer` | 17 |
| `failed_low` | 14 |
| `error` | 6 |
| `near_top_private_lift` | 4 |
| `severe_failure` | 3 |
| `near_top_public_drop` | 3 |
| `near_top_stable` | 3 |
| `private_best_hold` | 1 |
| `private_best_lift` | 1 |
| `unknown_private` | 1 |

## Operation Groups

### Adapter packaging

- Submissions: `1`
- Best private result: `0.86` from `20260605_slot4_mirzayasir_best_086_v16_remote_output`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-05 | `20260605_slot4_mirzayasir_best_086_v16_remote_output` | 0.86 | 0.86 | Private-best artifact; public signal was validated. |

### Evaluation error

- Submissions: `6`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-12 | `Notebook NemotronLoraForge / Version 1` |  |  | No valid score; operation resulted in evaluation failure. |
| 2026-06-08 | `Notebook finding nemo 50ced5 / Version 1` |  |  | No valid score; operation resulted in evaluation failure. |
| 2026-06-04 | `` |  |  | No valid score; operation resulted in evaluation failure. |
| 2026-06-04 | `` |  |  | No valid score; operation resulted in evaluation failure. |
| 2026-06-04 | `` |  |  | No valid score; operation resulted in evaluation failure. |
| 2026-06-03 | `20260603_slot1_tong_adapter_repack_db56ce42_stage2_retry` |  |  | No valid score; operation resulted in evaluation failure. |

### Finding Nemo variant packaging

- Submissions: `2`
- Best private result: `0.84` from `Notebook Nemotron Verify Finding Nemo | Version 1`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-08 | `Notebook Nemotron Verify Finding Nemo / Version 1` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-08 | `Notebook finding nemo 3adc97 / Version 1` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |

### Localcal LoRA-B scaling

- Submissions: `10`
- Best private result: `0.85` from `localcal_rohan_anchor_lmhead_loraB_x1.04_structure_preserved`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-07 | `localcal_rohan_anchor_lmhead_loraB_x1.25_structure_preserved` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-07 | `localcal_rohan_anchor_lmhead_loraB_x1.15_structure_preserved` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-06 | `localcal_rohan_anchor_lmhead_loraB_x1.04_structure_preserved` | 0.85 | 0.85 | Private 0.85; useful secondary route. |
| 2026-06-06 | `localcal_rohan_anchor_lmhead_loraB_x1.03_structure_preserved` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-06 | `localcal_rohan_anchor_lmhead_loraB_x1.05_structure_preserved` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-06 | `localcal_rohan_anchor_lmhead_loraB_x1.02_structure_preserved` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-06 | `localcal_rohan_anchor_lmhead_loraB_x1.01_structure_preserved` | 0.86 | 0.85 | Near-top private result but dropped from public by -0.01. |
| 2026-06-05 | `localcal_rohan_anchor_lmhead_loraB_x0.9975_structure_preserved` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-05 | `localcal_rohan_anchor_late_inproj_loraB_x0.9975_structure_preserved` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-04 | `localcal_rohan_anchor_inproj_loraB_x0.9975_structure_preserved` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |

### Merge/fusion/task arithmetic

- Submissions: `6`
- Best private result: `0.84` from `20260609_slot1_nemotron-s7-dare-merge_4f37c337`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-12 | `merge_v14_0.8_v5_0.2` | 0.70 | 0.72 | Private 0.72; failed or unstable route. |
| 2026-06-09 | `20260609_slot1_nemotron-s7-dare-merge_4f37c337` | 0.84 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-08 | `20260608_slot5_nemotron-s7-ties-sign-merge_b03e975e` | 0.84 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-06 | `20260606_slot4_stage7_keithtyser_taskarith_3b1d2fc3` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-06 | `slot2_dedquoc_svd_fusion_ccb88b2607ae` | 0.78 | 0.79 | Private 0.79; failed or unstable route. |
| 2026-06-05 | `20260605_slot3_rauffauzan_fusion_output_af996be0` | 0.86 | 0.83 | Private 0.83; weak transfer. |

### Other packaging/probe

- Submissions: `7`
- Best private result: `0.84` from `20260605_slot5_debatreyabiswas_086_v1_remote_output`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-08 | `20260608_slot2_nemotron-s8-answer-tail-512-v1_b79e16fc` | 0.27 | 0.24 | Private 0.24; severe failure. |
| 2026-06-05 | `Variance retry public 0.86 adapter v32 epoch 5` | 0.85 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-05 | `20260605_slot5_debatreyabiswas_086_v1_remote_output` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-04 | `20260604_slot2_akihiko_lora_exp1_lr1e4_r32_48680a75` | 0.50 | 0.55 | Private 0.55; severe failure. |
| 2026-06-04 | `` | 0.63 | 0.65 | Private 0.65; failed or unstable route. |
| 2026-06-03 | `public_lopure_amplify_top50_singular_values_v3` | 0.84 | 0.84 | Private 0.84; valid but not a final candidate. |
|  | `` |  |  | No privateScore available for this row. |

### Public high-score reproduction

- Submissions: `6`
- Best private result: `0.85` from `Submit own copy of Hammad 0.87 adapter`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-06 | `slot3_kuang_087_training_6b3f0b1397e7` | 0.63 | 0.65 | Private 0.65; failed or unstable route. |
| 2026-06-06 | `slot1_hammad_agi_for_medal_087_945fe257b622` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-05 | `Submit own copy of Kuang 0.87/0.88 adapter` | 0.62 | 0.65 | Private 0.65; failed or unstable route. |
| 2026-06-05 | `Submit own copy of Hammad 0.87 adapter` | 0.84 | 0.85 | Near-top private result and improved over public by +0.01. |
| 2026-06-05 | `Submit public AGI for medal 0.87 adapter` | 0.84 | 0.85 | Near-top private result and improved over public by +0.01. |
| 2026-06-03 | `public_kuangyicheng_087_training_v91` | 0.60 | 0.65 | Private 0.65; failed or unstable route. |

### Public notebook packaging/probe

- Submissions: `23`
- Best private result: `0.84` from `Notebook NemotronCOMP best 0.86 solution NVIDIA(under 5min) | Version 1`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-08 | `Notebook NemotronCOMP best 0.86 solution NVIDIA(under 5min) / Version 1` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-08 | `Direct submission from notebook` | 0.86 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-07 | `Direct submission from notebook` | 0.85 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-07 | `Notebook NemotronCOMP best 0.86 solution NVIDIA(under 5min) / Version 9` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-07 | `Direct submission from notebook` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-07 | `Notebook NemotronCOMP best 0.86 solution NVIDIA(under 5min) / Version 8` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-07 | `Direct submission from notebook` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-06 | `Notebook NemotronCOMP best 0.86 solution NVIDIA(under 5min) / Version 2` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-06 | `Direct submission from notebook` | 0.62 | 0.64 | Private 0.64; failed or unstable route. |
| 2026-06-06 | `Direct submission from notebook` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-06 | `Notebook NemotronCOMP best 0.86 solution NVIDIA(under 5min) / Version 1` | 0.85 | 0.82 | Private 0.82; weak transfer. |
| 2026-06-06 | `Direct submission from notebook` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-05 | `Submit public 0.86 adapter v32 epoch 5` | 0.86 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-04 | `Direct resubmit best v3 adapter` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-04 | `Notebook Tinker Adapter to Ready To Submit Adapter / Version 2` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-04 | `Notebook Tinker Adapter to Ready To Submit Adapter / Version 1` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-04 | `Notebook 0.86 Adapter Packaging Workflow / Version 1` | 0.85 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-04 | `Notebook LoRA Nvidia Nemotron Models with Pytorch / Version 3` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-04 | `Notebook LoRA Nvidia Nemotron Models with Pytorch / Version 2` | 0.84 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-04 | `Notebook Nemotron Tier-1 LoRA Baseline / Version 1` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-02 | `Notebook Nemotron Tier-1 LoRA Baseline / Version 1` | 0.85 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-02 | `Notebook NVIDIA_COMP b6fdb7 / Version 1` | 0.86 | 0.83 | Private 0.83; weak transfer. |
| 2026-05-31 | `Notebook Tinker Adapter to Ready To Submit Adapter / Version 1` | 0.86 | 0.83 | Private 0.83; weak transfer. |

### QR-SVD / adapter cleanup

- Submissions: `6`
- Best private result: `0.85` from `20260614_slot2_huikang_blocktopk_floor4_clean_probe`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-15 | `20260615_refine_psf_clean_qrsvd_valid_probe` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-14 | `20260614_slot2_huikang_blocktopk_floor4_clean_probe` | 0.85 | 0.85 | Private 0.85; useful secondary route. |
| 2026-06-14 | `20260614_asalhi_default20mirror_tailguard092_v1` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-12 | `Notebook Refine f05d8a / Version 1` | 0.86 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-03 | `backup_public_0.87_huikang_svd_from_own_kernel` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-03 | `public_0.87_huikang_svd_from_kernel_v3` | 0.84 | 0.85 | Near-top private result and improved over public by +0.01. |

### Rank-32 SVD adapter packaging

- Submissions: `1`
- Best private result: `0.86` from `Notebook finding nemo | Version 1`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-05-27 | `Notebook finding nemo / Version 1` | 0.84 | 0.86 | Private-best artifact; private exceeded public by +0.02. |

### RepairCal calibration

- Submissions: `6`
- Best private result: `0.84` from `20260615_repaircal_nojitter_s001925_center_fill_probe`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-15 | `20260615_repaircal_nojitter_s001925_center_fill_probe` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-14 | `20260614_slot3_repaircal_nojitter_s001975_center_refine_probe` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-13 | `20260613_slot5_repaircal_nojitter_s00195_center_stability_probe` | 0.86 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-13 | `20260613_slot4_repaircal_nojitter_s0021_upper_edge_probe` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-13 | `20260613_slot3_repaircal_nojitter_s0019_private_curve_midpoint` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-13 | `20260613_slot2_repaircal_nojitter_s0020_private_curve_probe` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |

### Replay/public custom route

- Submissions: `3`
- Best private result: `0.84` from `20260608_slot1_nemotron-s8-guarded-weak-replay-v1_6b54462e`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-08 | `20260608_slot1_nemotron-s8-guarded-weak-replay-v1_6b54462e` | 0.84 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-05 | `20260605_slot6_mohamed_replay_data_086_v4_remote_output` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |
| 2026-06-05 | `20260605_slot7_taha_custom_repo_086_v6_remote_output` | 0.86 | 0.84 | Public 0.86 did not transfer; private fell to 0.84. |

### Sparse-trust adapter modification/wrapper

- Submissions: `2`
- Best private result: `0.85` from `20260615_wrap_biohack_v62_public_sparse_trust_probe`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-15 | `20260615_wrap_biohack_v62_public_sparse_trust_probe` | 0.86 | 0.85 | Near-top private result but dropped from public by -0.01. |
| 2026-06-15 | `20260615_biohack_v62_alpha00085_sparse_trust_probe` | 0.86 | 0.83 | Private 0.83; weak transfer. |

### Symbolic-focused SFT

- Submissions: `3`
- Best private result: `0.85` from `symbolic2 lr12 v1 localcv825 symbolic-only validated`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-13 | `20260613_slot1_symbolic2_lr08_32_localcv825_private_diversity` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-05-27 | `symbolic focused public localcv824 validated` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-05-27 | `symbolic2 lr12 v1 localcv825 symbolic-only validated` | 0.86 | 0.85 | Near-top private result but dropped from public by -0.01. |

### Training/custom SFT

- Submissions: `16`
- Best private result: `0.85` from `20260608_slot4_nemotron-s7-seed-stability-replay_f5dde9e0`

| Date | Description | Public | Private | Operation Result |
| --- | --- | ---: | ---: | --- |
| 2026-06-15 | `20260615_wrap_vaibhav_custom_cot_public_sft_probe` | 0.57 | 0.57 | Private 0.57; severe failure. |
| 2026-06-12 | `Notebook Nvidia Nemotron Trained Models Submission / Version 3` | 0.70 | 0.71 | Private 0.71; failed or unstable route. |
| 2026-06-12 | `Notebook Nvidia Nemotron Trained Models Submission / Version 2` | 0.70 | 0.72 | Private 0.72; failed or unstable route. |
| 2026-06-08 | `20260608_slot4_nemotron-s7-seed-stability-replay_f5dde9e0` | 0.85 | 0.85 | Private 0.85; useful secondary route. |
| 2026-06-08 | `20260608_slot3_nemotron-s7-weak-protected-curriculum-v2_631a2bfb` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-07 | `20260607_slot5_nemotron-s7-mamba-inproj-specialist-v2_852e8025` | 0.81 | 0.82 | Private 0.82; weak transfer. |
| 2026-06-07 | `20260607_slot4_nemotron-s7-muon-full-v5-audited_2d42d0ad` | 0.84 | 0.85 | Near-top private result and improved over public by +0.01. |
| 2026-06-07 | `20260607_slot3_nemotron-s7-modulewise-delta-svd-r32_00d6bd3f` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-07 | `20260607_slot2_nemotron-s7-delta-space-svd-r32_b31b987c` | 0.85 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-07 | `20260607_slot1_nemotron-s7-protected-rehearsal_641c57f3` | 0.85 | 0.83 | Private 0.83; weak transfer. |
| 2026-06-03 | `v2_microtrain_shuffled_lr1e-7_4step_kernel_output` | 0.85 | 0.84 | Private 0.84; valid but not a final candidate. |
| 2026-06-02 | `Notebook Nvidia Nemotron Trained Models Submission b0fbfb / Version 2` | 0.70 | 0.69 | Private 0.69; failed or unstable route. |
| 2026-06-02 | `Notebook Nvidia Nemotron Trained Models Submission 4a1dde / Version 1` | 0.73 | 0.76 | Private 0.76; failed or unstable route. |
| 2026-06-02 | `Notebook Nvidia Nemotron Trained Models Submission bfaab0 / Version 1` | 0.73 | 0.76 | Private 0.76; failed or unstable route. |
| 2026-05-31 | `Notebook Nvidia Nemotron Trained Models Submission b0fbfb / Version 1` | 0.71 | 0.70 | Private 0.70; failed or unstable route. |
| 2026-05-27 | `Notebook Nvidia Nemotron Trained Models Submission / Version 1` | 0.69 | 0.71 | Private 0.71; failed or unstable route. |
