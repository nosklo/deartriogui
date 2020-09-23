import collections
import functools

import outcome
import trio

import threading
from dearpygui.dearpygui import *


# GLOBALS - they must be used because dearpygui does some evil magic with the callbacks.
_callbacks = collections.deque()
_callbacks_edit = threading.Lock()
_callbacks_wait = threading.Event()

_trio_func = None

results: outcome.Outcome = None
nursery: trio.Nursery = None


def run(trio_func):
    """
    Starts dearpygui while bound to the lifetime of a nursery with a trio function running.

    :param trio_func: the trio function to run
    :return: The results of the function, or None if the window is closed.
    """

    global _trio_func
    _trio_func = trio_func
    run_async_function(_wait_for_event, data=None, return_handler=_event_set)
    trio.lowlevel.start_guest_run(
        _run_trio_func,
        run_sync_soon_threadsafe=_run_sync_soon_threadsafe,
        done_callback=_stop_thread,
    )
    start_dearpygui()
    if results is not None:
        return results.unwrap()


def _canceller(arg1, arg2):
    nursery.cancel_scope.cancel()
    return False


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
        nursery.start_soon(async_func, sender, data, *args)
    return _async_callback


async def _run_trio_func(*args, **kwds):
    global nursery
    async with trio.open_nursery() as _nursery:
        nursery = _nursery
        set_exit_callback(_canceller)
        result = await _trio_func()
        set_exit_callback(None)
        return result


def _run_sync_soon_threadsafe(func):
    _callbacks.append(func)
    _callbacks_wait.set()


def _wait_for_event(func_type, func_data):
    _callbacks_wait.wait()


def _event_set(func_type, func_data):
    """Runs in main thread"""
    while _callbacks:
        _callbacks.popleft()()
    _callbacks_wait.clear()

    # start another waiting thread
    run_async_function(_wait_for_event, data=None, return_handler=_event_set)


def _stop_thread(_results=None):
    global results
    results = _results
    _callbacks.appendleft(stop_dearpygui)
    _callbacks_wait.set()


