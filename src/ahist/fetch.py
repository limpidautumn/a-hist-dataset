"""从第三方源拉取全市场 A 股行情快照。"""

from datetime import datetime
import akshare as ak

# 数据源 -> AKShare 接口：tx=腾讯，sina=新浪
_FETCHERS = {
    "tx": ak.stock_zh_a_spot_tx,
    "sina": ak.stock_zh_a_spot,
}


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

    stock_data = _FETCHERS[source]()
    print(stock_data.head())
    stock_data.to_csv(save_path, index=False)

    return stock_data


if __name__ == "__main__":
    fetch_spot("tx")
    fetch_spot("sina")
