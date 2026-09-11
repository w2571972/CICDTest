# 讓 `python -m game2048` 可以直接開始遊戲
from game2048.cli import main

raise SystemExit(main())
