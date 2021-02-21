from staircase.core.stairs import Stairs

from staircase.core.collections.functions import (
    aggregate,
    corr,
    cov,
    _max as max,
    _mean as mean,
    _median as median,
    _min as min,
    resample,
    sample,
)

from staircase.core.stats import hist_from_ecdf

from staircase.test_data import make_test_data

from staircase.constants import inf


def get_version():
    def get_version_post_py38():
        from importlib.metadata import version

        return version(__name__)

    def get_version_pre_py38():
        from pkg_resources import get_distribution

        return get_distribution(__name__).version

    def default_version():
        return "unknown"

    for func in (get_version_post_py38, get_version_pre_py38, default_version):
        try:
            return func()
        except Exception:
            pass


__version__ = get_version()
