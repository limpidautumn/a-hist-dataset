#!/usr/bin/env bash
# 本地冒烟测试：dry-run 拉取两个数据源，校验重命名后的 CSV 存在且非空。
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${repo}/src${PYTHONPATH:+:${PYTHONPATH}}"

# 优先使用仓库自带的虚拟环境
PY="${PYTHON:-python}"
[[ -x "${repo}/.venv/bin/python" ]] && PY="${repo}/.venv/bin/python"

work="$(mktemp -d)"
trap 'rm -rf "${work}"' EXIT
cd "${work}"

"${PY}" -m ahist.cli primary --dry-run

shopt -s nullglob
files=(stock_zh_a_hist_*.csv)
[[ ${#files[@]} -eq 2 ]] || { echo "FAIL: 期望 2 个 CSV，实际 ${#files[@]}" >&2; exit 1; }
for csv in "${files[@]}"; do
    [[ -s "${csv}" ]] || { echo "FAIL: ${csv} 为空" >&2; exit 1; }
    echo "OK: ${csv} ($(wc -l < "${csv}") 行)"
done
