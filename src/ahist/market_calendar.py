"""判断当前时间拉取到的行情快照属于哪个交易日。"""

from datetime import datetime, time, timedelta, timezone
from functools import cache

import akshare as ak

# A 股按北京时间交易，固定 UTC+8
TZ = timezone(timedelta(hours=8))

# A 股 09:30 开盘、15:00 收盘
_OPEN, _CLOSE = time(9, 30), time(15, 0)

# 盘状态
IN_SESSION, AFTER_CLOSE = "in_session", "after_close"


def session_state(ts, span=timedelta()):
    """返回自 ts 起、历时 span 的一次拉取所处的盘状态；开盘前视为上一交易日收盘后。"""
    if ts.time() < _CLOSE and (ts + span).time() >= _OPEN:
        return IN_SESSION  # 拉取窗口落在盘中（跨过开盘也算）
    return AFTER_CLOSE


@cache
def _trade_dates():
    """交易日历；缓存复用，避免反复请求。"""
    return ak.tool_trade_date_hist_sina()["trade_date"]


def trade_date_state(ts):
    """返回 (交易日, 盘状态)：交易日为此刻能拿到的最近一个收盘价所属的日子。"""
    day = ts.date()
    if ts.time() < _CLOSE:  # 当日尚未收盘，拿到的仍是上一交易日的收盘价
        day -= timedelta(days=1)
    return max(d for d in _trade_dates() if d <= day), session_state(ts)


def current_trade_date(now=None):
    """返回当前时刻所属的交易日，即此刻拉取能拿到的最近一个收盘价对应的交易日。

    :param now: 注入的当前时间（便于测试），默认取北京时间
    :return: datetime.date
    """
    return trade_date_state(now or datetime.now(TZ))[0]


if __name__ == "__main__":
    print(current_trade_date().strftime("%Y%m%d"))
