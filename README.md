# demo-githooks

## 集成测试

`tests/test_gitignore_check.sh` 验证 gitignore-check 行为（应忽略拒绝 / 非忽略允许）。

## Branch name check

`scripts/branch_name_check.py` validates a supplied name or the current Git branch:

```bash
python scripts/branch_name_check.py --branch feat/branch-name-check
python scripts/branch_name_check.py
python scripts/branch_name_check.py --branch feat/foo_bar
```

Valid names are `main`, `master`, or `feat/`, `fix/`, `chore/`, `epic/`, or `release/` followed by a lowercase alphanumeric slug with single hyphen separators. The command writes `ok: NAME` and exits `0` for a valid name; it writes an invalid-name error to stderr and exits `1` for a rule violation; it exits `2` when no current Git branch can be read.

```bash
python -m unittest tests/test_branch_name_check.py
```
