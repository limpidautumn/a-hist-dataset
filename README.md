# a-hist-dataset

An open dataset of full-market A-share quotes for every trading day, hosted on [Hugging Face](https://huggingface.co/datasets/LimpidAutumn/a-hist-dataset).

A GitHub Action fetches the closing quotes from Tencent and Sina via [AKShare](https://akshare.akfamily.xyz/) four times a day and appends them to the dataset.

## Files

- `data/daily/stock_zh_a_hist_{source}_{%Y%m%d}.csv` — one trading day (`tx` Tencent, `sina` Sina)
- `data/primary/stock_zh_a_hist_{source}_{%Y%m%d%H%M%S}.csv` — raw snapshots

## Usage

```python
from huggingface_hub import hf_hub_download
hf_hub_download("LimpidAutumn/a-hist-dataset", "data/daily/stock_zh_a_hist_tx_20260915.csv", repo_type="dataset")
```
