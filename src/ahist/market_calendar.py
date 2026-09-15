"""判断当前时间拉取到的行情快照属于哪个交易日。"""

from datetime import datetime, time, timedelta, timezone

import akshare as ak

# A 股按北京时间交易，固定 UTC+8
_TZ = timezone(timedelta(hours=8))

# A 股 15:00 收盘，只有收盘后拉取到的才是当日收盘价
_CLOSE = time(15, 0)


def current_trade_date(now=None):
    """返回当前时刻所属的交易日，即此刻拉取能拿到的最近一个收盘价对应的交易日。

    :param now: 注入的当前时间（便于测试），默认取北京时间
    :return: datetime.date
    """
    now = now or datetime.now(_TZ)
    # 未到收盘时间，当日还没有收盘价，回退到上一日再取最近交易日
    if now.time() < _CLOSE:
        now -= timedelta(days=1)
    trade_dates = ak.tool_trade_date_hist_sina()["trade_date"]
    return max(day for day in trade_dates if day <= now.date())


if __name__ == "__main__":
    print(current_trade_date().strftime("%Y%m%d"))
