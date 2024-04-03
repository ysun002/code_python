from score import Score


def test_constructor():
    """
    Test the constructor for score
    """
    s = Score()
    assert s.score_dict == {}
    assert s.sorted_dict == []


def test_add_player():
    """
    Test the add player fuction
    """
    s = Score()
    pl_name = "a"
    pl_score = 1
    s.add_player(pl_name, pl_score)
    assert s.score_dict == {"a": 1}


def test_sort_data():
    """
    Test the sort data fuction
    """
    s = Score()
    s.score_dict = {"a": 1, "b": 5}
    s.sort_the_data()
    assert s.sorted_dict == [('b', 5), ('a', 1)]
