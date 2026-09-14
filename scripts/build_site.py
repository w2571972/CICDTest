"""組裝要部署的網站。

把 web/ 的網頁和遊戲規則 src/game2048/board.py 放進同一個資料夾 _site/，
並把目前的 commit 版本號寫進網頁，方便對照「網站上跑的是哪一版」。

用法：python scripts/build_site.py
"""

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
PLACEHOLDER = "__VERSION__"


def commit_version() -> str:
    # GitHub Actions 會提供 GITHUB_SHA；在本機就直接問 git
    sha = os.environ.get("GITHUB_SHA")
    if not sha:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
            )
            sha = result.stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return "local"
    return sha[:7]


def main() -> None:
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.copytree(ROOT / "web", OUT)
    shutil.copy2(ROOT / "src" / "game2048" / "board.py", OUT / "board.py")

    index = OUT / "index.html"
    html = index.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        raise SystemExit(f"index.html 裡找不到 {PLACEHOLDER}，無法寫入版本號")
    version = commit_version()
    index.write_text(html.replace(PLACEHOLDER, version), encoding="utf-8")

    print(f"網站已組裝到 {OUT}（版本 {version}）")


if __name__ == "__main__":
    main()
