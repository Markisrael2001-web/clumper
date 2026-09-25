from clumper import Clumper


def test_group_by_four_columns_with_missing_combination():
    data = [
        {"a": 1, "b": 1, "c": 1, "d": 1, "value": 10},
        {"a": 1, "b": 1, "c": 1, "d": 2, "value": 20},
        {"a": 1, "b": 1, "c": 2, "d": 1, "value": 30},
        {"a": 2, "b": 1, "c": 1, "d": 1, "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("a", "b", "c", "d")
        .agg(total=("value", sum))
        .collect()
    )

    totals = {
        (row["a"], row["b"], row["c"], row["d"]): row["total"]
        for row in result
    }

    assert totals[(1, 1, 1, 1)] == 10
    assert totals[(1, 1, 1, 2)] == 20
    assert totals[(1, 1, 2, 1)] == 30
    assert totals[(2, 1, 1, 1)] == 40


def test_group_by_two_columns_with_multiple_aggregations():
    data = [
        {"grp_1": "a", "grp_2": "a", "value": 10},
        {"grp_1": "a", "grp_2": "a", "value": 20},
        {"grp_1": "a", "grp_2": "b", "value": 30},
        {"grp_1": "b", "grp_2": "a", "value": 40},
    ]

    result = (
        Clumper(data)
        .group_by("grp_1", "grp_2")
        .agg(
            total=("value", sum),
            count=("value", len),
        )
        .collect()
    )

    results = {
        (row["grp_1"], row["grp_2"]): (row["total"], row["count"])
        for row in result
    }

    assert results[("a", "a")] == (30, 2)
    assert results[("a", "b")] == (30, 1)
    assert results[("b", "a")] == (40, 1)

    #new line