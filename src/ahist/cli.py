"""GitHub Workflow 主程序：拉取全市场行情并上传到 HuggingFace 数据库。

用法：PYTHONPATH=src python -m ahist.cli --repo-id <user>/<dataset> --token <hf_token>
"""

import argparse
import os

from huggingface_hub import HfApi

from .market_calendar import current_trade_date
from .fetch import fetch_spot

# 需要拉取的数据源：腾讯、新浪
_SOURCES = ("tx", "sina")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", required=True, help="HuggingFace 数据库仓库 ID")
    parser.add_argument(
        "--token", default=os.environ.get("HF_TOKEN"), help="HuggingFace token，默认取 HF_TOKEN"
    )
    parser.add_argument("--data-dir", default="data", help="本地暂存目录")
    parser.add_argument("--dry-run", action="store_true", help="只拉取保存，不上传")
    args = parser.parse_args()

    date_str = current_trade_date().strftime("%Y%m%d")
    os.makedirs(args.data_dir, exist_ok=True)
    api = HfApi(token=args.token)

    for source in _SOURCES:
        # 文件名：stock_zh_a_hist_{source}_{%Y%m%d}.csv
        filename = f"stock_zh_a_hist_{source}_{date_str}.csv"
        save_path = os.path.join(args.data_dir, filename)
        fetch_spot(source, save_path)
        if not args.dry_run:
            # 上传到数据库的 data/ 目录
            api.upload_file(
                path_or_fileobj=save_path,
                path_in_repo=f"data/{filename}",
                repo_id=args.repo_id,
                repo_type="dataset",
            )
        print(f"{source} -> {save_path}")


if __name__ == "__main__":
    main()
