#!/usr/bin/env bash
# 本地冒烟测试：dry-run 拉取腾讯/新浪两个数据源，校验 CSV 存在且非空。
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="src${PYTHONPATH:+:${PYTHONPATH}}"

# 优先使用仓库自带的虚拟环境
PY="${PYTHON:-python}"
[[ -x .venv/bin/python ]] && PY=".venv/bin/python"

data_dir="$(mktemp -d)"
trap 'rm -rf "${data_dir}"' EXIT

trade_date="$("${PY}" -m ahist.market_calendar)"
echo "trade date: ${trade_date}"

"${PY}" -m ahist.cli --repo-id local/smoke --dry-run --data-dir "${data_dir}"

for source in tx sina; do
    csv="${data_dir}/stock_zh_a_hist_${source}_${trade_date}.csv"
    if [[ ! -s "${csv}" ]]; then
        echo "FAIL: ${csv} 缺失或为空" >&2
        exit 1
    fi
    echo "OK: ${csv} ($(wc -l < "${csv}") 行)"
done
