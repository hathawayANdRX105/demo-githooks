# demo-githooks

## hook 规范检查脚本

`scripts/hook-spec-check.sh` — 校验 commit message 前缀 + 拒绝缓存/临时文件。

```bash
./scripts/hook-spec-check.sh "feat: add check"      # exit 0
./scripts/hook-spec-check.sh "badmsg"               # exit 1
./scripts/hook-spec-check.sh --files src/a.pyc      # exit 1（拒绝缓存/临时文件）
./scripts/hook-spec-check.sh --files - < <(git diff --cached --name-only)  # stdin 模式
```
