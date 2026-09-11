import random

import pytest

from game2048.board import Game, add_random_tile, can_move, has_won, merge_line, move


# parametrize：同一個測試跑多組資料，每組在報告裡都會分開列出
@pytest.mark.parametrize(
    ("line", "expected", "score"),
    [
        ([0, 0, 0, 0], [0, 0, 0, 0], 0),
        ([2, 0, 0, 0], [2, 0, 0, 0], 0),
        ([0, 0, 0, 2], [2, 0, 0, 0], 0),
        ([2, 0, 2, 0], [4, 0, 0, 0], 4),
        ([2, 4, 8, 16], [2, 4, 8, 16], 0),
        # 每個方塊一回合只能合併一次
        ([2, 2, 2, 2], [4, 4, 0, 0], 8),
        ([2, 2, 4, 0], [4, 4, 0, 0], 4),
        # 從推的方向那一端開始合併
        ([2, 2, 2, 0], [4, 2, 0, 0], 4),
        ([8, 8, 0, 8], [16, 8, 0, 0], 16),
    ],
)
def test_merge_line(line, expected, score):
    assert merge_line(line) == (expected, score)


BOARD = [
    [2, 2, 0, 0],
    [0, 4, 0, 4],
    [2, 0, 0, 0],
    [2, 0, 0, 0],
]


def test_move_left():
    assert move(BOARD, "left") == (
        [
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 0, 0, 0],
        ],
        12,
    )


def test_move_right():
    assert move(BOARD, "right") == (
        [
            [0, 0, 0, 4],
            [0, 0, 0, 8],
            [0, 0, 0, 2],
            [0, 0, 0, 2],
        ],
        12,
    )


def test_move_up():
    assert move(BOARD, "up") == (
        [
            [4, 2, 0, 4],
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        4,
    )


def test_move_down():
    assert move(BOARD, "down") == (
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [4, 4, 0, 4],
        ],
        4,
    )


def test_move_does_not_change_original_board():
    before = [row[:] for row in BOARD]
    move(BOARD, "left")
    assert before == BOARD


def test_move_rejects_unknown_direction():
    with pytest.raises(ValueError):
        move(BOARD, "diagonal")


def test_can_move():
    full_no_pairs = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    assert not can_move(full_no_pairs)

    with_pair = [row[:] for row in full_no_pairs]
    with_pair[3][3] = 4  # 和上面的 4 相鄰
    assert can_move(with_pair)

    with_empty = [row[:] for row in full_no_pairs]
    with_empty[0][0] = 0
    assert can_move(with_empty)


def test_can_move_with_only_horizontal_pair():
    # 只有左上角的 2、2 是左右相鄰相同，上下都沒有相同的
    board = [
        [2, 2, 4, 8],
        [4, 8, 16, 32],
        [8, 16, 32, 64],
        [16, 32, 64, 128],
    ]
    assert can_move(board)


def test_add_random_tile_on_full_board():
    full = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    assert add_random_tile(full, random.Random(0)) is False


def test_has_won():
    board = [[0] * 4 for _ in range(4)]
    assert not has_won(board)
    board[1][2] = 2048
    assert has_won(board)


def count_tiles(board):
    return sum(1 for row in board for v in row if v)


def test_new_game_starts_with_two_tiles():
    game = Game(seed=1)
    assert count_tiles(game.board) == 2
    assert game.score == 0


def test_same_seed_gives_same_game():
    a, b = Game(seed=42), Game(seed=42)
    for direction in ["left", "up", "right", "down"]:
        a.play(direction)
        b.play(direction)
    assert a.board == b.board
    assert a.score == b.score


def test_play_adds_score_and_new_tile():
    game = Game(seed=1)
    game.board = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert game.play("left") is True
    assert game.score == 4
    assert count_tiles(game.board) == 2  # 合併後剩 1 個，再補 1 個新的


def test_play_that_changes_nothing_is_ignored():
    game = Game(seed=1)
    game.board = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert game.play("left") is False
    assert count_tiles(game.board) == 1  # 沒動就不能補新方塊
