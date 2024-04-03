from gamecontroller import GameController


def test_constructor():
    """
    Test the constructor for game controller
    """
    square_size = 100
    board_width = 8
    checker_num = 12
    gc = GameController(square_size, board_width)
    assert gc.width == board_width
    assert gc.lenth == board_width
    assert gc.checker_num == checker_num
    assert gc.square_size == square_size
    assert gc.orginal_x == 0
    assert gc.orginal_y == 0
    assert gc.origi_i == 0
    assert gc.origi_j == 0
    assert gc.current_checker is None
    assert gc.highlight_x == 0
    assert gc.highlight_y == 0
    assert len(gc.matrix) == board_width
    assert gc.legal_posi == []
    assert gc.drag is False
    assert gc.valid_jump == []
    assert gc.black_can_jump is False
    assert gc.black_valid_jump == []
    assert gc.remove_red == []
    assert gc.red_king_valid == []
    assert gc.num_black_checker == 0
    assert gc.num_red_checker == 0
    assert gc.step_count == 0
    assert gc.player_turn is True
    assert gc.end_game is False
    assert gc.black_win == "blank"
    assert gc.red_win == "blank"
    assert gc.both_draw == "blank"
    assert gc.player_score == 0
    assert gc.name == 0
    assert gc.start_write is True
    assert gc.countdown == 50


def test_mouse_click():
    """
    Test the mouse click function
    """
    square_size = 100
    board_width = 8
    checker_num = 12
    gc = GameController(square_size, board_width)
    mouseX = 50
    mouseY = 750
    gc.mouse_click(mouseX, mouseY)
    assert gc.drag is True


def test_check_jump():
    """
    Test the check_jump function
    """
    square_size = 100
    board_width = 8
    checker_num = 12
    gc = GameController(square_size, board_width)
    gc.check_jump()
    assert gc.valid_jump == []


def test_black_jump():
    """
    Test the black_jump function
    """
    square_size = 100
    board_width = 8
    checker_num = 12
    gc = GameController(square_size, board_width)
    assert gc.black_valid_jump == []


def test_convert_index():
    """
    Test the convert_index function
    """
    square_size = 100
    board_width = 8
    checker_num = 12
    gc = GameController(square_size, board_width)
    x = 50
    y = 100
    assert gc.convert_index(x, y) == (0, 1)
