import numpy as np
from sortedcontainers import SortedDict, SortedSet
import staircase as sc


def _sanitize_binary_operands(self, other, copy_other=False):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other)
    else:
        if copy_other:
            other = other.copy()
    return self.copy(), other


def _get_union_of_points(collection):
    def dict_common_points():
        return collection.values()

    def series_common_points():
        return collection.values

    def array_common_points():
        return collection

    for func in (dict_common_points, series_common_points, array_common_points):
        try:
            stairs_instances = func()
            points = []
            for stair_instance in stairs_instances:
                points += list(stair_instance._keys())
            return SortedSet(points)
        except (AttributeError, TypeError):
            pass
    raise TypeError(
        "Collection should be a tuple, list, numpy array, dict or pandas.Series."
    )


def _get_stairs_method(name):
    return {
        "mean": sc.core.stats.statistic.mean,
        "median": sc.core.stats.statistic.median,
        "mode": sc.core.stats.statistic.mode,
        "max": sc.core.stairs.Stairs.max,
        "min": sc.core.stairs.Stairs.min,
    }[name]


def _verify_window(left_delta, right_delta):
    zero = type(left_delta)(0)
    assert left_delta <= zero, "left_delta must not be positive"
    assert right_delta >= zero, "right_delta must not be negative"
    assert right_delta - left_delta > zero, "window length must be non-zero"


def _from_cumulative(init_value, cumulative):
    new_instance = sc.Stairs(init_value)
    new_instance._replace_sorted_dict(
        SortedDict(
            zip(
                cumulative.keys(),
                np.diff(np.array([init_value] + list(cumulative.values()))),
            )
        )
    )
    return new_instance._reduce()
