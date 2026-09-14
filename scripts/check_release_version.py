"""確認發版用的 tag 和 pyproject.toml 裡的版本號一致。

用法：python scripts/check_release_version.py v0.2.0
"""

import sys
import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("用法：python scripts/check_release_version.py v0.2.0")
    tag = sys.argv[1]
    version = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"]
    if tag != f"v{version}":
        raise SystemExit(
            f"tag {tag} 和 pyproject.toml 的版本 {version} 不一致。"
            f"請先把 pyproject.toml 改成對應版本，或改打 v{version}"
        )
    print(f"版本一致：{tag}")


if __name__ == "__main__":
    main()
