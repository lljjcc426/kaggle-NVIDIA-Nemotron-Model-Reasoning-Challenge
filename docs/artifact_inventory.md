# Artifact Inventory

## 收录内容

| 目录 | 内容 | 说明 |
| --- | --- | --- |
| `reports/` | 榜单、提交记录、派生统计表、模型 artifact manifest | 体积小、可审计、可复盘 |
| `metadata/` | 关键 Kaggle kernel metadata | 记录 notebook id、输入模型、GPU/Internet 配置 |
| `src/` | 清理后的关键代码路线 | 去除 notebook 展示文本、emoji、编码乱码和临时输出 |
| `docs/` | 赛题约束、最终结果、路线复盘 | 直接基于本地文件和 Kaggle CLI 快照 |

## 排除内容

| 类型 | 原因 |
| --- | --- |
| `adapter_model.safetensors` | 单文件约 3GB，不适合 GitHub，且可由 Kaggle model/dataset source 挂载 |
| `submission.zip` | 大体积二进制提交包，内容可由脚本重新生成 |
| Kaggle 缓存目录 | 环境相关，不具备复盘价值 |
| 临时 pull/output 目录 | 多为中间态或重复产物 |
| 原始 notebook 导出文本 | 包含展示性 markdown、emoji 和 Windows 编码乱码，不适合作为正式仓库内容 |
| 运行日志 | 大多为环境噪声或重复进度，不影响最终结论 |

## 关键来源

路线级分数汇总保存在 `reports/route_retrospective_summary.csv` 和 `reports/route_detailed_statistics.csv`，用于支撑 `docs/experiment_retrospective.md` 与 `docs/technical_postmortem.md` 中的“调整-效果-判断”分析。模型/adapter artifact 清单保存在 `reports/model_artifact_manifest.csv`。

| 路线 | Metadata |
| --- | --- |
| Mirza v16 | `metadata/mirza_v16_kernel-metadata.json` |
| Finding Nemo | `metadata/finding_nemo_kernel-metadata.json` |
| Finding Nemo 3adc97 | `metadata/finding_nemo_3adc97_kernel-metadata.json` |
| Nemotron Verify Finding Nemo | `metadata/nemotron_verify_finding_nemo_kernel-metadata.json` |
| Huikang Refine PSF Clean | `metadata/huikang_refine_psf_clean_kernel-metadata.json` |
| Kienngx RepairCal s001925 | `metadata/kienngx_repaircal_nojitter_strength001925_kernel-metadata.json` |
| Biohack wrapper | `metadata/wrap_biohack_v62_public_kernel-metadata.json` |

## 可复现入口

| 脚本 | 用途 |
| --- | --- |
| `src/package_mirza_v16_adapter.py` | 对 `assiabenazzouz/adappter-v32-epoch-5` adapter 做 rank 校验和 zip 包装 |
| `src/package_finding_nemo_rank32_svd.py` | 对 Finding Nemo/Kienngx 系 adapter 做 rank-32 SVD 转换和 zip 包装 |
| `src/package_huikang_refine_psf_clean.py` | Huikang/default20 Refine QR-SVD 路线 |
| `src/package_kienngx_repaircal_nojitter_strength001925.py` | Kienngx RepairCal no-jitter 路线 |
| `src/wrap_biohack_v62_public.py` | Biohack v62 public wrapper |
