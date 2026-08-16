#!/usr/bin/env bash
# gitignore-check.sh — 校验文件列表没有应被 .gitignore 忽略的路径（demo）
# 用法：printf '路径\n' | scripts/gitignore-check.sh -  或传路径参数
set -u
GI=".gitignore"
[ -f "$GI" ] || { echo "ok: no .gitignore (nothing to check)"; exit 0; }

banned=0
while IFS= read -r f; do
    [ -z "$f" ] && continue
    if git check-ignore -q "$f" 2>/dev/null; then
        echo "FAIL: $f is gitignored — must not be committed" >&2
        banned=1
    fi
done
[ $banned -eq 0 ] && echo "ok: no gitignored files" || exit 1
