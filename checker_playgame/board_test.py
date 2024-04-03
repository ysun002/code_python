from board import Board


def test_constructor():
    """
    Test the constructor for board
    """
    square_size = 100
    lenth = 8
    board = Board(square_size, lenth)
    empty_total = 0
    assert board.width == lenth
    assert board .lenth == lenth
    assert board.square_size == square_size
    assert board.x_posi == 0
    assert board.y_posi == 0


def test_add_checker():
    """
    Test the add checker function
    """
    square_size = 100
    lenth = 8
    board = Board(square_size, lenth)
    assert len(board.matrix) == lenth
