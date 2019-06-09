#!/usr/bin/env python
"""We don't really know how to work with asyncio so we will add here stupid helpers."""
import functools

def america_please_egzblein(func):
    @functools.wraps(func)
    async def wrapped(*args):
        try:
            return await func(*args)
        except Exception as exc:
            print("Exceptions :", exc)
            raise 
    return wrapped
