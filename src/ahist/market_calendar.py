"""判断当前时间拉取到的行情快照属于哪个交易日。"""

from datetime import datetime, timedelta, timezone

import akshare as ak

# A 股按北京时间交易，中国无夏令时，固定 UTC+8
_TZ = timezone(timedelta(hours=8))


def current_trade_date(now=None):
    """返回当前时刻所属的交易日，即不晚于今天的最近一个交易日。

    :param now: 注入的当前时间（便于测试），默认取北京时间
    :return: datetime.date
    """
    today = (now or datetime.now(_TZ)).date()
    trade_dates = ak.tool_trade_date_hist_sina()["trade_date"]
    return max(day for day in trade_dates if day <= today)


if __name__ == "__main__":
    print(current_trade_date().strftime("%Y%m%d"))
