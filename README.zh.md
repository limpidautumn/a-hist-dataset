# a-hist-dataset

每个交易日的全市场 A 股行情，以开放数据集形式托管在 [Hugging Face](https://huggingface.co/datasets/LimpidAutumn/a-hist-dataset)。

GitHub Action 每天四次通过 [AKShare](https://akshare.akfamily.xyz/) 拉取腾讯、新浪的收盘行情并追加到数据集。

## 文件

- `data/daily/stock_zh_a_hist_{source}_{%Y%m%d}.csv` — 某交易日的全市场行情（`tx` 腾讯、`sina` 新浪）
- `data/primary/stock_zh_a_hist_{source}_{%Y%m%d%H%M%S}.csv` — 原始快照

## 使用

```python
from huggingface_hub import hf_hub_download
hf_hub_download("LimpidAutumn/a-hist-dataset", "data/daily/stock_zh_a_hist_tx_20260915.csv", repo_type="dataset")
```
