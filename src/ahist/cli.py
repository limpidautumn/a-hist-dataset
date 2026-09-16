"""GitHub Action 主程序：拉取行情快照（primary）并维护每日链接（daily）。

用法：PYTHONPATH=src python -m ahist.cli {primary|daily} [--dry-run]
"""

import argparse
import os
from datetime import datetime, timedelta

from huggingface_hub import CommitOperationCopy, HfApi

from .fetch import fetch_spot
from .market_calendar import AFTER_CLOSE, TZ, current_trade_date, session_state

SOURCES = ("tx", "sina")  # 腾讯、新浪

# 单次拉取耗时上界（实测 tx≈25s、sina≈60s），用于判断拉取窗口是否跨过开盘
SPAN = timedelta(minutes=5)


def _start_time(path, prefix):
    """从 primary 文件名解析拉取起始时间。"""
    return datetime.strptime(path[len(prefix):-4], "%Y%m%d%H%M%S").replace(tzinfo=TZ)


def primary(api, repo_id, dry_run=False):
    """任务 1：拉取两个数据源并推送至 data/primary/。"""
    for source in SOURCES:
        ts = datetime.now(TZ).strftime("%Y%m%d%H%M%S")  # 每个源单独取一次时间
        name = f"stock_zh_a_hist_{source}_{ts}.csv"
        fetch_spot(source, name)
        path = f"data/primary/{name}"
        if not dry_run:
            api.upload_file(
                path_or_fileobj=name, path_in_repo=path, repo_id=repo_id, repo_type="dataset"
            )
        print(path)


def daily(api, repo_id, dry_run=False):
    """任务 2：把 data/daily/ 链接到上个交易日收盘状态的最新 primary 文件。"""
    date = current_trade_date().strftime("%Y%m%d")
    files = api.list_repo_files(repo_id, repo_type="dataset")
    for source in SOURCES:
        prefix = f"data/primary/stock_zh_a_hist_{source}_"
        latest = max(
            f
            for f in files
            if f.startswith(prefix)
            and session_state(_start_time(f, prefix), SPAN) == AFTER_CLOSE
        )
        path = f"data/daily/stock_zh_a_hist_{source}_{date}.csv"
        if not dry_run:
            api.create_commit(
                repo_id,
                [CommitOperationCopy(src_path_in_repo=latest, path_in_repo=path)],
                commit_message=f"link {path}",
                repo_type="dataset",
            )
        print(f"{path} -> {latest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("primary", "daily"))
    parser.add_argument("--repo-id", default=os.environ.get("HF_REPO_ID"))
    parser.add_argument("--token", default=os.environ.get("HF_TOKEN"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.repo_id and not args.dry_run:
        parser.error("缺少 --repo-id 或环境变量 HF_REPO_ID")
    {"primary": primary, "daily": daily}[args.task](
        HfApi(token=args.token), args.repo_id, args.dry_run
    )


if __name__ == "__main__":
    main()
