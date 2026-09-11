"""2048 的遊戲規則。

這裡只有資料和純函式，不讀鍵盤、不印畫面，所以每個函式都能直接寫測試。
"""

import random

SIZE = 4
WIN_TILE = 2048
DIRECTIONS = ("left", "right", "up", "down")

Board = list[list[int]]


def empty_cells(board: Board) -> list[tuple[int, int]]:
    return [(r, c) for r, row in enumerate(board) for c, v in enumerate(row) if v == 0]


def add_random_tile(board: Board, rng: random.Random) -> bool:
    """在隨機空格放一個 2（90%）或 4（10%）。沒有空格時回傳 False。"""
    cells = empty_cells(board)
    if not cells:
        return False
    r, c = rng.choice(cells)
    board[r][c] = 4 if rng.random() < 0.1 else 2
    return True


def new_board(rng: random.Random) -> Board:
    board = [[0] * SIZE for _ in range(SIZE)]
    add_random_tile(board, rng)
    add_random_tile(board, rng)
    return board


def merge_line(line: list[int]) -> tuple[list[int], int]:
    """把一列往左推並合併，回傳（新的一列, 這次得到的分數）。

    每個方塊一回合只能合併一次：[2, 2, 2, 2] 會變成 [4, 4, 0, 0]，不是 [8, 0, 0, 0]。
    """
    tiles = [v for v in line if v]
    merged: list[int] = []
    score = 0
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged.append(tiles[i] * 2)
            score += tiles[i] * 2
            i += 2
        else:
            merged.append(tiles[i])
            i += 1
    merged += [0] * (len(line) - len(merged))
    return merged, score


def _transpose(board: Board) -> Board:
    return [list(row) for row in zip(*board, strict=True)]


def _reverse(board: Board) -> Board:
    return [row[::-1] for row in board]


def move(board: Board, direction: str) -> tuple[Board, int]:
    """往某個方向移動，回傳（新盤面, 得分）。不會修改傳進來的 board。

    四個方向都轉換成「往左推」處理：上下先轉置，右和下先左右翻轉，推完再轉回來。
    """
    if direction not in DIRECTIONS:
        raise ValueError(f"不支援的方向：{direction!r}")

    b = [row[:] for row in board]
    if direction in ("up", "down"):
        b = _transpose(b)
    if direction in ("right", "down"):
        b = _reverse(b)

    rows: Board = []
    score = 0
    for row in b:
        merged, gained = merge_line(row)
        rows.append(merged)
        score += gained

    if direction in ("right", "down"):
        rows = _reverse(rows)
    if direction in ("up", "down"):
        rows = _transpose(rows)
    return rows, score


def can_move(board: Board) -> bool:
    """還有空格，或有相鄰的相同方塊，就還能移動。"""
    if empty_cells(board):
        return True
    for r in range(SIZE):
        for c in range(SIZE):
            if c + 1 < SIZE and board[r][c] == board[r][c + 1]:
                return True
            if r + 1 < SIZE and board[r][c] == board[r + 1][c]:
                return True
    return False


def has_won(board: Board) -> bool:
    return any(v >= WIN_TILE for row in board for v in row)


class Game:
    """一局遊戲的狀態。傳入 seed 可以讓隨機結果固定，測試時很好用。"""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.board = new_board(self.rng)
        self.score = 0

    def play(self, direction: str) -> bool:
        """走一步。盤面有變化才會加分、補新方塊，並回傳 True。"""
        new, gained = move(self.board, direction)
        if new == self.board:
            return False
        self.board = new
        self.score += gained
        add_random_tile(self.board, self.rng)
        return True

    @property
    def won(self) -> bool:
        return has_won(self.board)

    @property
    def over(self) -> bool:
        return not can_move(self.board)
