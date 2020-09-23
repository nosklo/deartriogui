import contextlib
import functools

from . import _runners
from dearpygui.dearpygui import end

__all__ = ['async_callback', 'container']

def async_callback(async_func, *args):
    """
    Wraps an async function, so that it can be used as a dearpygui callback.
    The function will be called in deartriogui's window lifetime nursery.
    `sender` and `data` parameters are forwarded.

    :param async_func: the function to call
    :param args: args to pass to the function
    :return: the wrapped callback
    """
    @functools.wraps(async_func)
    def _async_callback(sender, data):
        _runners.nursery.start_soon(async_func, sender, data, *args)
    return _async_callback


@contextlib.contextmanager
def container(f, name, *args, **kwds):
    yield f(name, *args, **kwds)
    end()
