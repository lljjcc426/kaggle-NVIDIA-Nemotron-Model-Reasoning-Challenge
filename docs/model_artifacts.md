# Model And Adapter Artifacts

本仓库允许发布模型或 adapter 相关材料，但不发布 Kaggle `submission.zip`。`submission.zip` 是提交打包产物，和模型权重本体、adapter 来源、生成脚本、hash 证据不是同一类 artifact。

## 当前收录

| 类型 | 是否进入普通 Git | 说明 |
| --- | --- | --- |
| 代码脚本 | 是 | `src/` 中保留 packaging、rank-32 SVD、RepairCal、Refine、Biohack wrapper 等核心逻辑 |
| Kaggle kernel metadata | 是 | `metadata/` 中保留 notebook id、输入模型、GPU/Internet 配置 |
| 分数和复盘表 | 是 | `reports/` 中保留 submissions、leaderboard、路线统计和模型 artifact manifest |
| adapter config | 可进入普通 Git | 小文件，可随具体模型目录补充 |
| `adapter_model.safetensors` | 只建议 Git LFS 或 GitHub Release | 典型大小约 3GB，不适合普通 Git blob |
| `submission.zip` | 否 | 已在 `.gitignore` 中排除 |

## LFS 策略

仓库已添加 `.gitattributes`，对 `.safetensors`、`.bin`、`.pt`、`.pth`、`.ckpt` 使用 Git LFS。发布 adapter 权重前应确认 Git LFS quota 和远端权限，再显式添加对应文件。GitHub 对普通 Git 大文件有明确限制，相关规则见 GitHub Docs: [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。

普通 Git 仓库仍保留 `submission.zip` 忽略规则，避免把一次性提交包误传。模型权重的发布单位应是 adapter 权重、config、README、hash 和来源说明，而不是 Kaggle submission zip。

## Artifact Manifest

模型/adapter 级别清单在 `reports/model_artifact_manifest.csv`。该表记录：

- route
- source or local path
- public/private score
- weight or zip size
- SHA256
- artifact status
- notes

当前私榜最高两个 artifact：

| Artifact | Public | Private | Source |
| --- | ---: | ---: | --- |
| Mirza v16 adapter | 0.86 | 0.86 | `assiabenazzouz/adappter-v32-epoch-5/adapter` |
| Finding Nemo original adapter | 0.84 | 0.86 | `kienngx/nemotron-nano-30b-trained/Triton/tinker-adapter/1` |
