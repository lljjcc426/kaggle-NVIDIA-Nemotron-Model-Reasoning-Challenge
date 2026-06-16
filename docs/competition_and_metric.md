# 赛题与评分机制

## 任务

比赛要求为 NVIDIA Nemotron-3-Nano-30B-A3B-BF16 提交一个 LoRA adapter。Kaggle 评测端将 adapter 加载到基座模型，并对隐藏测试题进行确定性推理。模型输出需要把最终答案放入 LaTeX `\boxed{}` 中；评分脚本优先提取 boxed 内容，也会回退到若干启发式答案提取规则。

## 提交约束

| 约束 | 数值 |
| --- | --- |
| 文件 | `submission.zip` |
| zip 根目录 | `adapter_config.json`, `adapter_model.safetensors` |
| LoRA rank | `<= 32` |
| 推理引擎 | vLLM |
| `temperature` | `0.0` |
| `top_p` | `1.0` |
| `max_tokens` | `7680` |
| `max_model_len` | `8192` |
| `max_lora_rank` | `32` |

这些约束决定了有效路线主要集中在 adapter 选择、rank-32 转换、轻量校准和提交包装上。超过 rank 限制、zip 根目录不正确、adapter config 不兼容或权重命名不匹配都会直接导致失败或低分。

## 数据分布

训练集包含 9500 条样本，六类题型接近平衡：

| Family | Count |
| --- | ---: |
| bit manipulation | 1602 |
| gravity | 1597 |
| unit conversion | 1594 |
| cipher | 1576 |
| numeral system | 1576 |
| equation | 1555 |

任务族平衡意味着单一题型过拟合路线在私榜上的波动风险更高。封榜后结果也验证了这一点：多条针对公榜半区稳定的微调或校准路线在私榜回落。

## 公榜与私榜

公榜使用隐藏测试集的一部分，最终排名由另一部分私榜测试集决定。本队复盘采用封榜后 Kaggle CLI 揭示的 `privateScore` 作为核心依据；赛前公榜排序只作为历史信号，不作为最终结论。
