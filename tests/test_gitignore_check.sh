#!/usr/bin/env bash
# 集成测试：gitignore-check 行为验证
set -u; cd "$(dirname "$0")/.." || exit 1
fail=0
run() { printf '%s\n' "$1" | ./scripts/gitignore-check.sh - >/dev/null 2>&1; [ $? -eq "$2" ] || { echo "FAIL: $1 (want $2)"; fail=1; }; }
run '.oi/config.toml' 1   # gitignored → 拒绝
run 'scripts/gitignore-check.sh' 0  # 不忽略 → 允许
run 'src/main.c' 0
exit $fail
