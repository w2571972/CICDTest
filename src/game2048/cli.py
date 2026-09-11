"""終端機介面：讀取按鍵、印出盤面。遊戲規則都在 board.py。"""

from collections.abc import Callable

from game2048.board import Game

KEYS = {"w": "up", "a": "left", "s": "down", "d": "right"}
HELP = "w/a/s/d 移動，q 離開"


def render(game: Game) -> str:
    rows = ["".join(f"{v or '.':>6}" for v in row) for row in game.board]
    return "\n".join([f"分數：{game.score}", *rows])


def main(seed: int | None = None, input_fn: Callable[[str], str] = input) -> int:
    """開始一局遊戲。input_fn 可以換成假的輸入，讓測試不用真的敲鍵盤。"""
    game = Game(seed)
    announced_win = False
    print(HELP)
    while True:
        print(render(game))
        if game.won and not announced_win:
            print("恭喜拼出 2048！可以繼續玩，按 q 離開。")
            announced_win = True
        if game.over:
            print(f"遊戲結束！最後分數：{game.score}")
            return 0

        try:
            key = input_fn("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if key == "q":
            return 0
        if key not in KEYS:
            print(f"看不懂的按鍵，{HELP}")
        elif not game.play(KEYS[key]):
            print("這個方向動不了，換個方向試試")
