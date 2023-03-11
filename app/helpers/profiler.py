"""Modulo de profiling"""

import contextlib
import cProfile
import io
import pstats

# pylint: disable=invalid-name, print-used


@contextlib.contextmanager
def profile():
    """Context manager que realiza un print de los datos de profile de un bloque de codigo"""
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats()
    # uncomment this to see who's calling what
    # ps.print_callers()
    print(s.getvalue())
