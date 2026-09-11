from game2048.board import Game
from game2048.cli import main, render


def fake_input(*keys):
    """模擬玩家依序按下這些鍵。"""
    it = iter(keys)
    return lambda _prompt: next(it)


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
