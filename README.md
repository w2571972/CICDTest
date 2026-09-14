# 2048 × CI/CD 練習

終端機版的 2048 小遊戲，用來一步一步練習 CI/CD。

## 玩遊戲

**網頁版**：<https://w2571972.github.io/CICDTest/>（main 通過 CI 後自動部署）

**終端機版**：

```bash
python -m game2048
```

用 `w` `a` `s` `d` 移動，`q` 離開。

## 開發環境

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS / Linux：source .venv/bin/activate
pip install -e ".[dev]"
```

推送前先在本機跑一次 CI 會做的檢查：

```bash
ruff check .           # 找出程式問題
ruff format .          # 自動整理排版
pytest -v --cov        # 執行測試並計算覆蓋率（低於 95% 會失敗）
```

在本機預覽網頁版（CD 部署的就是這個 `_site` 資料夾）：

```bash
python scripts/build_site.py
python -m http.server 8000 --directory _site   # 打開 http://localhost:8000
```

## 專案結構

```
src/game2048/
  board.py        遊戲規則（純函式，好測試）
  cli.py          終端機介面（讀按鍵、印盤面）
tests/            pytest 測試
web/index.html    網頁版介面（用 Pyodide 在瀏覽器執行 board.py）
scripts/
  build_site.py   組裝要部署的網站到 _site/
.github/workflows/
  ci.yml          CI/CD 設定：檢查 → 組裝網站 → 部署（只有 main）
pyproject.toml    專案設定、相依套件、pytest 與 ruff 設定
```

## 學習路線

- [x] **第 1 關：CI 基本款**：推送或發 PR 時自動跑 ruff 和 pytest
- [x] **第 2 關：分支保護**：在 GitHub 設定 main 必須通過 CI 才能合併，然後故意寫壞一個測試，看 PR 被擋下來
- [x] **第 3 關：矩陣測試**：同時在 Python 3.11、3.12、3.13，以及 Windows 和 Linux 上測試
- [x] **第 4 關：測試覆蓋率**：用 pytest-cov 計算測試覆蓋率，低於門檻就讓 CI 失敗
- [ ] **第 5 關：CD 部署網頁版**：用 Pyodide 讓同一份 `board.py` 在瀏覽器裡執行，main 通過 CI 後自動部署到 GitHub Pages
- [ ] **第 6 關：自動發版**：推送 `v0.2.0` 這類 tag 時，自動打包並建立 GitHub Release
- [ ] **第 7 關：Dependabot**：自動提出套件更新的 PR，由 CI 驗證更新有沒有弄壞東西
