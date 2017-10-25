"""
Responsible of the profiling of the chaosmonkey engine.

It has a contextmanager to wrap a call and dump the results.
"""
from contextlib import contextmanager
import cProfile

PROFILER_FILE_PATH = '/tmp/profile.prof'


@contextmanager
def profile_ctx(profiling):
    """
    Wrapper around to isolate responbability of profiling in a contextmanager
    """
    if profiling:
        pr = cProfile.Profile()
        pr.enable()
    yield
    if profiling:
        pr.disable()
        pr.dump_stats(PROFILER_FILE_PATH)
