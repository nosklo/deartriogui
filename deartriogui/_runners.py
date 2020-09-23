import collections

import outcome
import trio

import threading
from dearpygui.dearpygui import *


_callbacks = collections.deque()
_callbacks_edit = threading.Lock()
_callbacks_wait = threading.Event()

_trio_func = None

results: outcome.Outcome = None


def run(trio_func):
    """Starts dearpygui while bound to the lifetime of a trio function."""

    global _trio_func
    _trio_func = trio_func
    run_async_function(_wait_for_event, data=None, return_handler=_event_set)
    trio.lowlevel.start_guest_run(
        _run_trio_func,
        run_sync_soon_threadsafe=_run_sync_soon_threadsafe,
        done_callback=_stop_thread,
    )
    start_dearpygui()
    return results.unwrap()


async def _run_trio_func(*args, **kwds):
    async with trio.open_nursery() as nursery:
        return await _trio_func()


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


