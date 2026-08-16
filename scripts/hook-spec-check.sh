#!/usr/bin/env bash
# hook-spec-check.sh — 简单的 hook 规范检查（demo）
#
# 两种用法：
#   1) 校验 commit message 前缀（feat|fix|chore|docs，大小写不敏感）
#        ./scripts/hook-spec-check.sh "feat: add check"     # exit 0
#        ./scripts/hook-spec-check.sh "badmsg"              # exit 1
#   2) 检查文件路径列表，拒绝缓存/临时文件
#        ./scripts/hook-spec-check.sh --files src/a.pyc __pycache__/x.tmp   # exit 1
#        printf 'a.pyc\n__pycache__/b\n' | ./scripts/hook-spec-check.sh --files -   # exit 1
set -u

PREFIX_RE='^(feat|fix|chore|docs)(\([^)]*\))?!?: .+'
BANNED_RE='(^|/)(__pycache__/|.*\.pyc$|.*\.tmp$)'

check_commit() {
    local msg="$1"
    # Lowercase for case-insensitive prefix match (bash =~ has no /i flag).
    if [[ "${msg,,}" =~ $PREFIX_RE ]]; then
        echo "ok: commit message prefix valid"
        return 0
    fi
    echo "FAIL: commit message must start with feat|fix|chore|docs (e.g. \"feat: ...\")" >&2
    return 1
}

check_files() {
    local bad=0
    local f
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        if [[ "$f" =~ $BANNED_RE ]]; then
            echo "FAIL: banned file in commit: $f" >&2
            bad=1
        fi
    done
    if [[ $bad -eq 0 ]]; then
        echo "ok: no banned files"
        return 0
    fi
    return 1
}

case "${1:-}" in
    -h|--help)
        sed -n '2,9p' "$0"
        exit 0
        ;;
    --files)
        shift
        if [[ "${1:-}" == "-" ]]; then
            check_files
        else
            printf '%s\n' "$@" | check_files
        fi
        ;;
    "")
        echo "usage: hook-spec-check.sh <commit-message> | --files <paths...|->" >&2
        exit 2
        ;;
    *)
        check_commit "$1"
        ;;
esac
