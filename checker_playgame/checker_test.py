from checker import Checker


def test_constructor():
    """
    Test the constructor for black checker
    """
    circle_x = 50
    circle_y = 50
    checker = Checker(circle_x, circle_y)
    square_size = 100
    SMALL_FACTOR = 0.9
    radius = 90
    assert checker.square_size == square_size
    assert checker.radius == radius
    assert checker.king is False
    assert checker.circle_x == circle_x
    assert checker.circle_y == circle_y
    assert checker.color == 0
    assert checker.can_move is True
    assert checker.can_jump is False
