"""从第三方源拉取全市场 A 股行情快照。"""

from datetime import datetime
from time import sleep
import akshare as ak

# 数据源 -> AKShare 接口：tx=腾讯，sina=新浪
_FETCHERS = {
    "tx": ak.stock_zh_a_spot_tx,
    "sina": ak.stock_zh_a_spot,
}


# 第三方行情接口偶发超时，失败后等待并重试，避免一次网络抖动导致任务失败
_RETRIES = 3
_RETRY_DELAY = 5


def _fetch(source):
    """调用数据源接口，失败时重试，最后一次仍失败则抛出。"""
    for attempt in range(_RETRIES):
        try:
            return _FETCHERS[source]()
        except Exception as exc:
            if attempt == _RETRIES - 1:
                raise
            print(f"{source} fetch failed ({exc}), retrying...")
            sleep(_RETRY_DELAY)


def fetch_spot(source="tx", save_path=None):
    """拉取 source 源的全市场行情并保存为 CSV，返回 DataFrame。

    :param source: 'tx'（腾讯）或 'sina'（新浪）
    :param save_path: 保存路径；为空时按当前时间自动命名
    """
    if source not in _FETCHERS:
        raise ValueError(f"Unsupported source: {source}")

    if save_path is None:
        # 默认文件名：stock_zh_a_spot_{source}_{%Y%m%d%H%M%S}.csv
        save_path = (
            f"stock_zh_a_spot_{source}_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        )

    stock_data = _fetch(source)
    print(stock_data.head())
    stock_data.to_csv(save_path, index=False)

    return stock_data


if __name__ == "__main__":
    fetch_spot("tx")
    fetch_spot("sina")
