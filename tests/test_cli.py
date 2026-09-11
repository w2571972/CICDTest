from game2048.board import Game
from game2048.cli import main, render


def fake_input(*keys):
    """模擬玩家依序按下這些鍵。"""
    it = iter(keys)
    return lambda _prompt: next(it)


def game_with_board(board):
    """建立一局遊戲，並換成指定的盤面。"""
    game = Game(seed=1)
    game.board = board
    return game


def test_win_message(capsys):
    board = [
        [2048, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    main(input_fn=fake_input("q"), game=game_with_board(board))
    assert "恭喜" in capsys.readouterr().out


def test_game_over_message(capsys):
    board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    # 不給任何按鍵：遊戲一開始就結束，main() 不應該要求輸入
    assert main(input_fn=fake_input(), game=game_with_board(board)) == 0
    assert "遊戲結束" in capsys.readouterr().out


def test_cannot_move_message(capsys):
    board = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    main(input_fn=fake_input("a", "q"), game=game_with_board(board))
    assert "動不了" in capsys.readouterr().out


def test_successful_move_updates_score(capsys):
    board = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    main(input_fn=fake_input("a", "q"), game=game_with_board(board))
    assert "分數：4" in capsys.readouterr().out


def test_render_shows_score_and_board():
    game = Game(seed=1)
    game.score = 128
    text = render(game)
    assert "分數：128" in text
    assert len(text.splitlines()) == 5  # 分數一行加上 4 列盤面


def test_quit_with_q():
    assert main(seed=1, input_fn=fake_input("q")) == 0


def test_unknown_key_shows_help(capsys):
    main(seed=1, input_fn=fake_input("x", "q"))
    assert "看不懂的按鍵" in capsys.readouterr().out


def test_end_of_input_exits_cleanly():
    def no_more_input(_prompt):
        raise EOFError

    assert main(seed=1, input_fn=no_more_input) == 0
