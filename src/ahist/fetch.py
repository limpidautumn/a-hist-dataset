from datetime import datetime
import akshare as ak

_FETCHERS = {
    "tx": ak.stock_zh_a_spot_tx,
    "sina": ak.stock_zh_a_spot,
}


def fetch_spot(source="tx", save_path=None):
    if source not in _FETCHERS:
        raise ValueError(f"Unsupported source: {source}")

    if save_path is None:
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
